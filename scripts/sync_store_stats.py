"""
Syncs Microsoft Store Analytics for SC Utility Suite
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
    "USB Flasher": "9P9NBFS7PMJB"
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

def get_oauth_token():
    tenant_id = os.environ.get("MSSTORE_TENANT_ID")
    client_id = os.environ.get("MSSTORE_CLIENT_ID")
    client_secret = os.environ.get("MSSTORE_CLIENT_SECRET")
    
    # Fallback to local file if run locally
    if not (tenant_id and client_id and client_secret):
        local_path = r"C:\Users\Martin\Documents\SC Software Keys\msstore-analytics.json"
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
                tenant_id = creds.get("tenant_id")
                client_id = creds.get("client_id")
                client_secret = creds.get("client_secret")
                
    if not (tenant_id and client_id and client_secret):
        raise ValueError("Missing MS Store API credentials in environment or local key file.")
        
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

def main():
    token = get_oauth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    end_date = datetime.utcnow().strftime("%Y-%m-%d")
    start_date = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    total_acquisitions = 0
    total_installs = 0
    total_crashes = 0
    
    market_counts = {}
    os_counts = {}
    apps_data = []
    
    for app_name, app_id in APPS.items():
        time.sleep(1.2)
        acq_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/acquisitions?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        acq_data = call_api(acq_url, headers)
        acq_count = sum(item.get("acquisitionQuantity", 0) for item in acq_data.get("Value", []))
        
        time.sleep(1.2)
        fail_url = f"https://manage.devcenter.microsoft.com/v1.0/my/analytics/failurehits?applicationId={app_id}&startDate={start_date}&endDate={end_date}"
        fail_data = call_api(fail_url, headers)
        fail_count = sum(item.get("failureCount", 0) for item in fail_data.get("Value", []))
        
        time.sleep(1.2)
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
        
        apps_data.append({
            "name": app_name,
            "product_id": app_id,
            "acquisitions": acq_count,
            "installs": inst_count,
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
        
    output_payload = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "date_range": f"{start_date} to {end_date}",
        "summary": {
            "total_acquisitions": total_acquisitions,
            "total_installs": total_installs,
            "total_crashes": total_crashes,
            "apps_tracked": len(APPS)
        },
        "apps": apps_data,
        "markets": markets_formatted,
        "os_breakdown": os_formatted
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    out_file = os.path.join(root_dir, "store-stats.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)
        
    print(f"Store analytics successfully synced to {out_file}")
    print(f"Total Acquisitions: {total_acquisitions}, Total Installs: {total_installs}")

if __name__ == "__main__":
    main()
