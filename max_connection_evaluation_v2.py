import requests
from datetime import datetime, timedelta, time
import time as tm

# 1️⃣ API Key
API_KEY = input("🔑 Enter your Meraki API Key: ")
headers = {"X-Cisco-Meraki-API-Key": API_KEY}

# 2️⃣ Lister les organisations
orgs = requests.get("https://api.meraki.com/api/v1/organizations", headers=headers).json()
print("\n🏢 Available organizations:")
for i, org in enumerate(orgs, 1):
    print(f"{i}. {org['name']} ({org['id']})")
org_choice = int(input("➡️  Select organization number: "))
ORG_ID = orgs[org_choice-1]['id']

# 3️⃣ Lister les réseaux
networks = requests.get(f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/networks", headers=headers).json()
print("\n🌐 Available networks:")
for i, net in enumerate(networks, 1):
    print(f"{i}. {net['name']} ({net['id']})")
print(f"{len(networks)+1}. All networks")  # option tous
net_choice = int(input("➡️  Select network number: "))

# Déterminer le ou les networks et le label pour l'affichage
if net_choice == len(networks)+1:
    NETWORKS = networks
    selected_network_label = "All networks"
    all_networks_mode = True
else:
    NETWORKS = [networks[net_choice-1]]
    selected_network_label = networks[net_choice-1]['name']
    all_networks_mode = False

# 4️⃣ Plage de dates
start_date_str = input("📅 Start date (YYYY-MM-DD): ")
end_date_str = input("📅 End date (YYYY-MM-DD): ")

# 5️⃣ Plage horaire active
start_hour = int(input("⏰ Start hour (0-23): "))
end_hour = int(input("⏰ End hour (0-23): "))

# 6️⃣ Intervalle et estimation
interval_minutes = int(input("⏱ Snapshot interval in minutes: "))
estimated_snapshots = int((end_hour - start_hour) * 60 / interval_minutes)
print(f"ℹ️ Estimated snapshots per network for this range: {estimated_snapshots}")

# 7️⃣ Calcul du pic par jour
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
delta_days = (end_date - start_date).days + 1

max_lookback = datetime.utcnow() - timedelta(days=31)
results = {}

for day_offset in range(delta_days):
    current_day = start_date + timedelta(days=day_offset)
    daily_max = 0
    daily_max_time = None
    
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, interval_minutes):
            t0 = datetime.combine(current_day, time(hour, minute))
            
            if t0 < max_lookback:
                print(f"⚠️ Skipping {t0}, too far in the past (max 31 days).")
                continue
            
            t0_str = t0.strftime("%Y-%m-%dT%H:%M:%SZ")
            snapshot_sum = 0
            
            for net in NETWORKS:
                network_id = net['id']
                try:
                    resp = requests.get(
                        f"https://api.meraki.com/api/v1/networks/{network_id}/clients",
                        headers=headers,
                        params={"t0": t0_str, "statuses[]": "Online", "perPage": 5000}
                    )
                    resp.raise_for_status()
                    clients = resp.json()
                    snapshot_sum += len(clients)
                    tm.sleep(0.12)
                except requests.HTTPError as e:
                    if e.response.status_code == 400:
                        print(f"⚠️ Warning: Invalid snapshot at {t0_str}, skipping.")
                    else:
                        print(f"❌ Error at {t0_str}: {e}")
            
            if snapshot_sum > daily_max:
                daily_max = snapshot_sum
                daily_max_time = t0_str
    
    results[current_day.strftime('%Y-%m-%d')] = (daily_max, daily_max_time)

# 8️⃣ Affichage du résultat
print(f"\n📊 === Daily max clients for {selected_network_label} network ===")
for date_str, (max_clients, t0_str) in results.items():
    print(f"{date_str}: {max_clients} clients max at {t0_str}")
