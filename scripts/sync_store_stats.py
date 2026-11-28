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

# The four paid apps (sold as the app itself, so their Store sales are paid acquisitions, not add-ons).
PAID_APPS = {
    "Creator Forge": {"store": "9P18Z18SGV8F", "snap": "sc-creator-forge", "gumroad": "SC Creator Forge"},
    "FileFlow": {"store": "9P55JCHSDK2V", "snap": "sc-file-flow", "gumroad": "SC FileFlow"},
    "PaperTrail": {"store": "9P2K4281M9S2", "snap": "sc-paper-trail", "gumroad": "SC PaperTrail"},
    "ROM & Disc Smith": {"store": "9NV49B669CKN", "snap": "sc-rom-disc-smith", "gumroad": "SC ROM & Disc Smith"},
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

def call_api(url, headers, max_retries=6, base_delay=5.0):
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
    "Creator Forge": "sc-creator-forge",
    "FileFlow": "sc-file-flow",
    "PaperTrail": "sc-paper-trail",
    "ROM & Disc Smith": "sc-rom-disc-smith",
}


def previous_payload_section(name):
    """The section from the last published ecosystem-data.json (kept when a source cannot be read this run)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ecosystem-data.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get(name)
    except (OSError, ValueError):
        return None


def merge_ledger(old, fresh, start_date, ok):
    """Running all-time totals. Partner Center only answers for the last 90 days, so each day's count is kept here
    ({"YYYY-MM-DD|...": count}) once it leaves that window. Days inside the window are replaced by the fresh answer;
    if this run's call failed (ok=False) the previous ledger is kept untouched."""
    old = old or {}
    if not ok:
        return dict(old)
    merged = {k: v for k, v in old.items() if k[:10] < start_date}
    for k, v in fresh.items():
        merged[k] = merged.get(k, 0) + v
    return merged


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
    snaps, os_totals, country_totals, total = [], {}, {}, 0
    previous = {s["snap"]: s for s in (previous_payload_section("snap") or {}).get("snaps", [])}
    failures = 0
    for app, snap in SNAPS.items():
        try:
            # Snap publishes each day's figures with a lag: asking only for "yesterday" often returns NO DATA early in the
            # day. Ask for a week and use the newest day that has figures.
            start = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
            out = subprocess.run(["snapcraft", "metrics", snap, "--name", "installed_base_by_operating_system", "--start", start, "--format", "json"],
                                 capture_output=True, text=True, timeout=180)
            data = json.loads(out.stdout) if out.returncode == 0 else {}
            if out.returncode != 0:
                # Say why (Snap's own message; never the credentials), and keep the last good figure for this snap.
                reason = (out.stderr or out.stdout or "").strip().splitlines()
                print(f"Snap Store: metrics for {snap} failed (exit {out.returncode}): {reason[-1][:200] if reason else 'no message'}")
        except (subprocess.SubprocessError, ValueError) as e:
            print(f"Snap Store: metrics for {snap} failed: {type(e).__name__}")
            data = {}
        if not data.get("series"):
            print(f"Snap Store: no figures for {snap}; reply was: {(out.stdout if 'out' in dir() else '')[:160]!r}")
        if not data.get("series") and snap in previous:
            failures += 1
            kept = previous[snap]
            snaps.append(kept); total += kept.get("installs", 0)
            continue
        installs = 0
        buckets = data.get("buckets") or []
        # Newest day that has been published (a zero is a real figure; only missing days are skipped).
        day = next((k for k in range(len(buckets) - 1, -1, -1)
                    if any(k < len(sr.get("values") or []) and (sr.get("values") or [])[k] is not None for sr in data.get("series", []))), len(buckets) - 1)
        for series in data.get("series", []):
            values = series.get("values") or []
            latest = (values[day] if 0 <= day < len(values) else 0) or 0
            installs += latest
            os_totals[series.get("name", "?")] = os_totals.get(series.get("name", "?"), 0) + latest
        snaps.append({"name": app, "snap": snap, "installs": installs, "as_of": buckets[day] if 0 <= day < len(buckets) else ""})
        # Same newest day, split by country (Snap's installed_base_by_country); feeds the Audience countries panel.
        try:
            cout = subprocess.run(["snapcraft", "metrics", snap, "--name", "installed_base_by_country", "--start", start, "--format", "json"],
                                  capture_output=True, text=True, timeout=180)
            cdata = json.loads(cout.stdout) if cout.returncode == 0 else {}
        except (subprocess.SubprocessError, ValueError):
            cdata = {}
        cb = cdata.get("buckets") or []
        cday = next((k for k in range(len(cb) - 1, -1, -1)
                     if any(k < len(sr.get("values") or []) and (sr.get("values") or [])[k] is not None for sr in cdata.get("series", []))), -1)
        for series in cdata.get("series", []) if cday >= 0 else []:
            values = series.get("values") or []
            n = (values[cday] if cday < len(values) else 0) or 0
            code = (series.get("name") or "").upper()
            if n and code: country_totals[code] = country_totals.get(code, 0) + n
        total += installs
    if failures == len(SNAPS):   # nothing read this run: keep the last published section as it was
        print("Snap Store: no metrics could be read; keeping the last published snap numbers.")
        return previous_payload_section("snap") or {"configured": False, "total_installs": 0, "snaps": [], "os_breakdown": []}
    os_list = [{"os": k, "count": v} for k, v in sorted(os_totals.items(), key=lambda x: x[1], reverse=True)]
    if not os_list: os_list = (previous_payload_section("snap") or {}).get("os_breakdown", [])
    countries = [{"code": k, "count": v} for k, v in sorted(country_totals.items(), key=lambda x: x[1], reverse=True)]
    if not countries: countries = (previous_payload_section("snap") or {}).get("countries", [])
    return {"configured": True, "total_installs": total, "snaps": snaps, "os_breakdown": os_list, "countries": countries}


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
    old_ledger = previous_payload_section("store_ledger") or {}
    ledger = {}
    # Store sales older than the 90-day window are carried over from the last payload so revenue never shrinks.
    old_store_sales = [s for s in (previous_payload_section("sales_history") or [])
                       if s.get("source") == "Microsoft Store" and (s.get("date") or "9")[:10] < start_date]
    
    for app_name, app_id in APPS.items():
        time.sleep(1.2)
        # Acquisitions
        acq_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/acquisitions?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        acq_data = call_api(acq_url, headers)
        acq_fresh = {}
        for item in acq_data.get("Value", []):
            d = (item.get("date") or "")[:10] or "?"
            acq_fresh[d] = acq_fresh.get(d, 0) + (item.get("acquisitionQuantity", 0) or 0)
        
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
        fail_fresh = {}
        for item in fail_data.get("Value", []):
            d = (item.get("date") or "")[:10] or "?"
            fail_fresh[d] = fail_fresh.get(d, 0) + (item.get("failureCount", 0) or 0)
        
        time.sleep(1.2)
        # Installs
        inst_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/installs?applicationId={app_id}&startDate={start_date}&endDate={end_date}&aggregationLevel=day&groupby=date,market,osVersion"
        inst_data = call_api(inst_url, headers)
        inst_fresh = {}
        for item in inst_data.get("Value", []):
            k = f"{(item.get('date') or '')[:10] or '?'}|{item.get('market') or 'Unknown'}|{item.get('osVersion') or 'Unknown'}"
            inst_fresh[k] = inst_fresh.get(k, 0) + (item.get("successfulInstallCount", 0) or 0)

        prev = old_ledger.get(app_id, {})
        ledger[app_id] = {
            "installs": merge_ledger(prev.get("installs"), inst_fresh, start_date, "error" not in inst_data),
            "acquisitions": merge_ledger(prev.get("acquisitions"), acq_fresh, start_date, "error" not in acq_data),
            "failures": merge_ledger(prev.get("failures"), fail_fresh, start_date, "error" not in fail_data),
        }
        acq_count = sum(ledger[app_id]["acquisitions"].values())
        fail_count = sum(ledger[app_id]["failures"].values())
        inst_count = sum(ledger[app_id]["installs"].values())
        for k, cnt in ledger[app_id]["installs"].items():
            _, m, osv = k.split("|", 2)
            market_counts[m] = market_counts.get(m, 0) + cnt
            os_counts[osv] = os_counts.get(osv, 0) + cnt

        for s in old_store_sales:
            if s.get("product_id") == app_id:
                store_sales.append(s)
                inapp_count += s.get("quantity", 0)
                inapp_rev += s.get("revenue_usd", 0.0)
            
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
        
    # Paid apps: a sale is a paid acquisition (purchasePriceUSDAmount > 0); free/promotional ones are owner tests.
    paid_apps = []
    for app_name, ids in PAID_APPS.items():
        app_id = ids["store"]
        time.sleep(1.2)
        acq = call_api(f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/acquisitions?applicationId={app_id}&startDate={start_date}&endDate={end_date}", headers).get("Value", [])
        sold, revenue = 0, 0.0
        for s in old_store_sales:
            if s.get("product_id") == app_id:
                store_sales.append(s); sold += s.get("quantity", 0); revenue += s.get("revenue_usd", 0.0)
        for item in acq:
            qty = item.get("acquisitionQuantity", 0) or 0
            price = float(item.get("purchasePriceUSDAmount") or 0.0)
            if qty <= 0 or price <= 0 or "promo" in str(item.get("acquisitionType") or "").lower():
                continue
            sold += qty; revenue += round(qty * price, 2)
            m_code = (item.get("market") or "").upper()
            store_sales.append({"source": "Microsoft Store", "app": app_name, "product_id": app_id, "addon_name": f"SC {app_name} (app purchase)",
                                "addon_id": "", "date": (item.get("date") or end_date)[:10], "market": m_code or "Store",
                                "country": COUNTRY_MAP.get(m_code, m_code or "Microsoft Store"), "quantity": qty, "revenue_usd": round(qty * price, 2), "os": ""})
        time.sleep(1.2)
        inst_resp = call_api(f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/installs?applicationId={app_id}&startDate={start_date}&endDate={end_date}&aggregationLevel=day&groupby=date,market", headers)
        time.sleep(1.2)
        fail_resp = call_api(f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/failurehits?applicationId={app_id}&startDate={start_date}&endDate={end_date}", headers)
        inst_fresh, fail_fresh = {}, {}
        for i in inst_resp.get("Value", []):
            k = f"{(i.get('date') or '')[:10] or '?'}|{i.get('market') or 'Unknown'}"
            inst_fresh[k] = inst_fresh.get(k, 0) + (i.get("successfulInstallCount", 0) or 0)
        for i in fail_resp.get("Value", []):
            d = (i.get("date") or "")[:10] or "?"
            fail_fresh[d] = fail_fresh.get(d, 0) + (i.get("failureCount", 0) or 0)
        prev = old_ledger.get(app_id, {})
        ledger[app_id] = {"installs": merge_ledger(prev.get("installs"), inst_fresh, start_date, "error" not in inst_resp),
                          "failures": merge_ledger(prev.get("failures"), fail_fresh, start_date, "error" not in fail_resp)}
        paid_apps.append({"name": app_name, "store_id": app_id, "snap": ids["snap"], "gumroad_product": ids["gumroad"],
                          "store_sales": sold, "store_revenue_usd": round(revenue, 2),
                          "store_installs": sum(ledger[app_id]["installs"].values()),
                          "crashes": sum(ledger[app_id]["failures"].values())})

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
        "date_range": f"all time to {end_date}",
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
        "paid_apps": paid_apps,
        "snap": fetch_snap_stats(),
        "github": fetch_github_downloads(),
        "store_ledger": ledger
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
