# 🧠 Meraki API - Daily Max Clients Snapshot

This Python script analyzes the **maximum number of connected clients** across one or more Meraki networks during a given day.  
It periodically queries the Meraki Dashboard API and identifies the **peak client count** for each day.

---

## 🚀 Features

- 🔑 API key–based authentication  
- 🏢 Interactive organization selection  
- 🌐 Choose one network or **all networks**  
- 📅 Define a custom date range (up to 31 days)  
- ⏰ Select active hours (e.g., 8 AM–6 PM)  
- ⏱ Choose snapshot interval (in minutes)  
- 📊 Displays **daily peak client count** and **timestamp of the peak**  
- ⚙️ Automatic rate-limit handling (10 requests per second)

---

## 🧩 Requirements

- Python 3.8 or higher  
- Python packages:
  ```bash
  pip install requests
  ```
- A valid **Meraki API key** with read access to your organization and networks.

---

## 🧠 Usage

1. **Clone** this repository or copy the script into a local file, e.g.:
   ```
   max_connection_evaluation.py
   ```

2. **Run** the script:
   ```bash
   python max_connection_evaluation.py
   ```

3. **Enter the requested information**:
   - Your API key  
   - Organization to analyze  
   - Network (or “All networks”)  
   - Date range and time window  
   - Snapshot interval (in minutes)

4. The script will output a summary such as:
   ```
   📊 === Daily max clients for Chris. network ===
   2025-10-20: 44 clients max at 2025-10-20T14:25:00Z
   2025-10-21: 42 clients max at 2025-10-21T13:40:00Z
   ```

---

## ⚠️ Limitations

- The Meraki API only supports a **31-day lookback window**.  
- The smaller the interval, the more API calls are required.  
  Example: a full 8-hour day with 5-minute intervals = 96 snapshots per network.  
- Retrieving results across multiple networks may take several minutes.

---

## 💡 Tips

- Use **5–15 minute** intervals for a good accuracy/performance balance.  
- If analyzing many networks, run the script overnight to avoid API throttling.  
- You can fine-tune the rate limit delay (`time.sleep(0.12)`) if needed.

---

## 📦 Example Timing Estimate

| Duration | Interval | Snapshots per network | Estimated time (1 network) |
|-----------|-----------|-----------------------|-----------------------------|
| 8 hours   | 5 min     | 96                    | ~30–45 seconds              |
| 8 hours   | 10 min    | 48                    | ~15–20 seconds              |

---
