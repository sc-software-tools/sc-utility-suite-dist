"""
Syncs Microsoft Store and Gumroad Analytics for SC Utility Suite
Outputs store-stats.json for the GitHub Pages Command Center dashboard.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
import requests

APPS = {
    "Archive Unpacker": "9NXS3LDTBRX8",
    "Dup Scrub": "9NL51TH9QR3M",
    "HEIC Studio": "9N4F9K6G90HK",
    "Media Trim": "9PC1HVN60QBP",
    "PDF Knife": "9NQLSS021G6T",
    "Screen Lens": "9N7V2FVFL4BN",
    "USB Flasher": "9P9NBFS7PMJB",
    "SC Utility Suite": "9NDSBW5TZ90G"
}

COUNTRY_MAP = {
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "NL": "Netherlands",
    "JP": "Japan",
    "TW": "Taiwan",
    "RU": "Russia",
    "TN": "Tunisia",
    "BA": "Bosnia and Herzegovina",
    "KH": "Cambodia",
    "AZ": "Azerbaijan",
    "CA": "Canada",
    "AU": "Australia",
    "IN": "India",
    "BR": "Brazil",
    "IT": "Italy",
    "ES": "Spain",
    "KR": "South Korea",
    "CN": "China"
}

def get_msstore_token():
    tenant_id = os.environ.get("MSSTORE_TENANT_ID")
    client_id = os.environ.get("MSSTORE_CLIENT_ID")
    client_secret = os.environ.get("MSSTORE_CLIENT_SECRET")
    
    if not (tenant_id and client_id and client_secret):
        local_path = r"C:\Users\Martin\Documents\SC Software Keys\msstore-analytics.json"
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
                tenant_id = creds.get("tenant_id")
                client_id = creds.get("client_id")
                client_secret = creds.get("client_secret")
                
    if not (tenant_id and client_id and client_secret):
        raise ValueError("Missing MS Store API credentials.")
        
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "https://manage.devcenter.microsoft.com"
    }
    
    resp = requests.post(token_url, data=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Authentication failed (HTTP {resp.status_code}): {resp.text}")
        
    return resp.json()["access_token"]

def call_api(url, headers, max_retries=4, base_delay=2.0):
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                time.sleep(base_delay * (attempt + 1))
            elif resp.status_code == 404:
                return {"Value": []}
            else:
                return {"error": f"HTTP {resp.status_code}"}
        except requests.RequestException:
            time.sleep(base_delay)
    return {"error": "Max retries exceeded"}

def record_quantity(item):
    for key in ("inAppAcquisitionQuantity", "acquisitionQuantity", "quantity", "orderQuantity"):
        val = item.get(key)
        if isinstance(val, (int, float)) and val > 0:
            return int(val)
    return 0

SNAPS = {
    "Archive Unpacker": "sc-archive-unpacker",
    "Dup Scrub": "sc-dup-scrub",
    "HEIC Studio": "sc-heic-studio",
    "Media Trim": "sc-media-trim",
    "PDF Knife": "sc-pdf-knife",
    "Screen Lens": "sc-screen-lens",
    "USB Flasher": "sc-usb-flasher",
    "SC Utility Suite": "sc-utility-suite",
}


def previous_payload_section(name):
    """The section from the last published ecosystem-data.json (kept when a source cannot be read this run)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ecosystem-data.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get(name)
    except (OSError, ValueError):
        return None


def fetch_github_downloads():
    """Download counts for every release asset (server-side, with the workflow's GITHUB_TOKEN, so visitors' browsers
    never hit GitHub's 60-requests-per-hour anonymous limit). Keeps the last published numbers if GitHub fails."""
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    try:
        resp = requests.get("https://api.github.com/repos/sc-software-tools/sc-utility-suite-dist/releases?per_page=100", headers=headers, timeout=30)
        resp.raise_for_status()
        releases = [{"tag_name": r.get("tag_name", ""), "published_at": r.get("published_at", ""),
                     "assets": [{"name": a.get("name", ""), "download_count": a.get("download_count", 0)} for a in r.get("assets", [])]}
                    for r in resp.json()]
        return {"releases": releases, "fetched": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
    except Exception as exc:
        print(f"GitHub downloads: {exc}; keeping the last published numbers.")
        return previous_payload_section("github") or {"releases": []}


def fetch_snap_stats():
    """Active Snap Store installs per snap (latest day of installed_base_by_operating_system) via `snapcraft metrics`.
    Needs SNAPCRAFT_STORE_CREDENTIALS (a metrics-only exported login). Without it the last published numbers are kept."""
    import shutil
    import subprocess
    if not os.environ.get("SNAPCRAFT_STORE_CREDENTIALS") or not shutil.which("snapcraft"):
        print("Snap Store: no credentials or snapcraft on this runner; keeping the last published snap numbers.")
        return previous_payload_section("snap") or {"configured": False, "total_installs": 0, "snaps": [], "os_breakdown": []}
    snaps, os_totals, total = [], {}, 0
    for app, snap in SNAPS.items():
        try:
            out = subprocess.run(["snapcraft", "metrics", snap, "--name", "installed_base_by_operating_system", "--format", "json"],
                                 capture_output=True, text=True, timeout=180)
            data = json.loads(out.stdout) if out.returncode == 0 else {}
        except (subprocess.SubprocessError, ValueError):
            data = {}
        installs = 0
        for series in data.get("series", []):
            latest = (series.get("values") or [0])[-1] or 0
            installs += latest
            os_totals[series.get("name", "?")] = os_totals.get(series.get("name", "?"), 0) + latest
        snaps.append({"name": app, "snap": snap, "installs": installs, "as_of": (data.get("buckets") or [""])[-1]})
        total += installs
    os_list = [{"os": k, "count": v} for k, v in sorted(os_totals.items(), key=lambda x: x[1], reverse=True)]
    return {"configured": True, "total_installs": total, "snaps": snaps, "os_breakdown": os_list}


def fetch_gumroad_stats():
    token = os.environ.get("GUMROAD_ACCESS_TOKEN")
    if not token:
        local_key = r"C:\Users\Martin\Documents\SC Software Keys\gumroad-token.txt"
        if os.path.exists(local_key):
            with open(local_key, "r", encoding="utf-8") as f:
                token = f.read().strip()
                
    if not token:
        return {"configured": False, "total_sales": 0, "total_revenue_usd": 0.0, "products": [], "recent_sales": []}
        
    try:
        def gumroad_pages(endpoint, key, limit=20):
            # Gumroad pages its lists (10 products / 10 sales per page); follow next_page_key.
            items, page_key, status = [], None, 200
            for _ in range(limit):
                params = {"access_token": token}
                if page_key:
                    params["page_key"] = page_key
                r = requests.get(f"https://api.gumroad.com/v2/{endpoint}", params=params, timeout=20)
                status = r.status_code
                if status != 200:
                    break
                body = r.json()
                items += body.get(key, [])
                page_key = body.get("next_page_key")
                if not page_key:
                    break
            return items, status

        all_products, status = gumroad_pages("products", "products")
        if status == 200 or all_products:
            # Drafts (unreleased apps) are not on sale; leave them off the stats page.
            products = [p for p in all_products if p.get("published") and not p.get("deleted")]
            total_sales = 0
            total_cents = 0
            prod_list = []
            for p in products:
                sales = p.get("sales_count", 0)
                cents = p.get("sales_usd_cents", 0)
                total_sales += sales
                total_cents += cents
                prod_list.append({
                    "name": p.get("name"),
                    "sales": sales,
                    "revenue_usd": round(cents / 100.0, 2),
                    "price": p.get("formatted_price")
                })

            recent_sales = []
            try:
                sales, _ = gumroad_pages("sales", "sales", limit=5)
                if sales:
                    for s in sales[:50]:
                        if s.get("refunded") or s.get("chargedback"):
                            continue
                        price_cents = s.get("price", 0)
                        code = (s.get("country_iso2") or "").upper()
                        recent_sales.append({
                            "source": "Gumroad",
                            "app": s.get("product_name") or "SC Utility Suite PRO",
                            "date": (s.get("created_at") or "")[:10],
                            "market": code or "Web",
                            "country": s.get("country") or COUNTRY_MAP.get(code, code or "Direct Web"),
                            "quantity": int(s.get("quantity") or 1),
                            "revenue_usd": round(price_cents / 100.0, 2),
                            "currency": (s.get("currency_symbol") or "$"),
                            # Where the buyer came from: in-app buy links carry utm_source=app, utm_medium=<os>,
                            # utm_campaign=<app permalink> (or suite-/cross- prefixed); no tag means web/Discover.
                            "utm_source": s.get("utm_source") or "",
                            "utm_medium": s.get("utm_medium") or "",
                            "utm_campaign": s.get("utm_campaign") or "",
                            "referrer": s.get("referrer") or "",
                            "discover": bool(s.get("discover_fee_charged"))
                        })
            except Exception:
                pass

            return {
                "configured": True,
                "total_sales": total_sales,
                "total_revenue_usd": round(total_cents / 100.0, 2),
                "products": prod_list,
                "recent_sales": recent_sales
            }
        else:
            return {"configured": False, "error": f"HTTP {status}", "total_sales": 0, "total_revenue_usd": 0.0, "products": [], "recent_sales": []}
    except Exception as e:
        return {"configured": False, "error": str(e), "total_sales": 0, "total_revenue_usd": 0.0, "products": [], "recent_sales": []}

def main():
    token = get_msstore_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    end_date = datetime.utcnow().strftime("%Y-%m-%d")
    start_date = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    total_acquisitions = 0
    total_installs = 0
    total_crashes = 0
    total_inapp = 0
    promo_redemptions = 0
    total_inapp_revenue = 0.0
    
    market_counts = {}
    os_counts = {}
    apps_data = []
    store_sales = []
    
    for app_name, app_id in APPS.items():
        time.sleep(1.2)
        # Acquisitions
        acq_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/acquisitions?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        acq_data = call_api(acq_url, headers)
        acq_count = sum(item.get("acquisitionQuantity", 0) for item in acq_data.get("Value", []))
        
        time.sleep(1.2)
        # In-app purchases (Add-ons)
        # Note: Partner Center returns purchasePriceUSDAmount (the unit price in USD, e.g. £3.29 = $4.42)
        # even on rows where acquisitionQuantity is 0 (such as a declined/cancelled checkout attempt).
        # Only completed purchases (qty > 0) count toward revenue!
        inapp_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/inappacquisitions?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        inapp_data = call_api(inapp_url, headers)
        inapp_records = inapp_data.get("Value", [])
        inapp_count = 0
        inapp_rev = 0.0

        for item in inapp_records:
            qty = record_quantity(item)
            unit_price = float(item.get("purchasePriceUSDAmount") or 0.0)
            # Every add-on is paid ($3.99 / $19.99): a $0 acquisition is a free promotional-code redemption (owner
            # testing), not an upgrade sale, so it stays out of the counts, revenue and sales history.
            if unit_price <= 0 or "promo" in str(item.get("acquisitionType") or "").lower():
                promo_redemptions += qty
                continue
            if qty > 0:
                row_rev = round(qty * unit_price, 2) if unit_price > 0 else 0.0
                inapp_count += qty
                inapp_rev += row_rev
                m_code = (item.get("market") or "").upper()
                store_sales.append({
                    "source": "Microsoft Store",
                    "app": app_name,
                    "product_id": app_id,
                    "addon_name": item.get("inAppProductName") or f"{app_name} PRO",
                    "addon_id": item.get("inAppProductId") or item.get("storeId") or "",
                    "date": (item.get("date") or item.get("startDate") or end_date)[:10],
                    "market": m_code or "Store",
                    "country": COUNTRY_MAP.get(m_code, m_code or "Microsoft Store"),
                    "quantity": qty,
                    "revenue_usd": row_rev,
                    "os": item.get("osVersion") or ""
                })
        
        time.sleep(1.2)
        # Failures
        fail_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/failurehits?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        fail_data = call_api(fail_url, headers)
        fail_count = sum(item.get("failureCount", 0) for item in fail_data.get("Value", []))
        
        time.sleep(1.2)
        # Installs
        inst_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/installs?applicationId={app_id}&startDate={start_date}&endDate={end_date}&groupby=market,deviceType,osVersion,packageVersion"
        inst_data = call_api(inst_url, headers)
        inst_records = inst_data.get("Value", [])
        inst_count = sum(item.get("successfulInstallCount", 0) for item in inst_records)
        
        for item in inst_records:
            cnt = item.get("successfulInstallCount", 0)
            m = item.get("market") or "Unknown"
            osv = item.get("osVersion") or "Unknown"
            market_counts[m] = market_counts.get(m, 0) + cnt
            os_counts[osv] = os_counts.get(osv, 0) + cnt
            
        total_acquisitions += acq_count
        total_installs += inst_count
        total_crashes += fail_count
        total_inapp += inapp_count
        total_inapp_revenue += inapp_rev
        
        apps_data.append({
            "name": app_name,
            "product_id": app_id,
            "acquisitions": acq_count,
            "installs": inst_count,
            "inapp_purchases": inapp_count,
            "inapp_revenue_usd": round(inapp_rev, 2),
            "crashes": fail_count
        })
        
    markets_formatted = []
    for code, cnt in sorted(market_counts.items(), key=lambda x: x[1], reverse=True):
        markets_formatted.append({
            "code": code,
            "country": COUNTRY_MAP.get(code, code),
            "count": cnt
        })
        
    os_formatted = []
    for osv, cnt in sorted(os_counts.items(), key=lambda x: x[1], reverse=True):
        os_formatted.append({
            "os": osv,
            "count": cnt,
            "percent": round((cnt / total_installs * 100), 1) if total_installs > 0 else 0
        })
        
    gumroad_data = fetch_gumroad_stats()
    combined_sales = sorted(
        store_sales + gumroad_data.get("recent_sales", []),
        key=lambda s: s.get("date", ""),
        reverse=True
    )
    
    output_payload = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "date_range": f"{start_date} to {end_date}",
        "summary": {
            "total_acquisitions": total_acquisitions,
            "total_installs": total_installs,
            "total_crashes": total_crashes,
            "total_inapp_purchases": total_inapp,
            "total_inapp_revenue_usd": round(total_inapp_revenue, 2),
            "apps_tracked": len(APPS)
        },
        "apps": apps_data,
        "sales_history": combined_sales,
        "markets": markets_formatted,
        "os_breakdown": os_formatted,
        "gumroad": gumroad_data,
        "snap": fetch_snap_stats(),
        "github": fetch_github_downloads()
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    for fname in ("store-stats.json", "ecosystem-data.json"):
        out_file = os.path.join(root_dir, fname)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2)

    stats_html_path = os.path.join(root_dir, "stats.html")
    if os.path.exists(stats_html_path):
        import re
        with open(stats_html_path, "r", encoding="utf-8") as f:
            html_text = f.read()
        embedded_js = "/* AUTO_SYNC_DATA_START */\n    var EMBEDDED_STORE_DATA = " + json.dumps(output_payload) + ";\n    /* AUTO_SYNC_DATA_END */"
        html_text_new = re.sub(
            r"/\* AUTO_SYNC_DATA_START \*/[\s\S]*?/\* AUTO_SYNC_DATA_END \*/",
            lambda _: embedded_js,
            html_text,
            count=1
        )
        if html_text_new != html_text:
            with open(stats_html_path, "w", encoding="utf-8") as f:
                f.write(html_text_new)
        
    print(f"Store analytics successfully synced to store-stats.json, ecosystem-data.json, and stats.html")
    print(f"Acquisitions: {total_acquisitions}, Installs: {total_installs}, InApp: {total_inapp} (excluded {promo_redemptions} promotional-code redemptions)")

if __name__ == "__main__":
    main()
