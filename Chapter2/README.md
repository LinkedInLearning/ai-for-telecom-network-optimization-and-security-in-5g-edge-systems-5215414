
Self Healing : Block the IPs which are flagged in the NRF Log

# Make sure `df` already exists and anomaly detection has been run

# Step 1: Regenerate original category mapping
df['src_ip'] = df['src_ip'].astype('category')  # Just to be safe
src_ip_mapping = dict(enumerate(df['src_ip'].cat.categories))

# Step 2: Find repeated offenders
anomalies = df[df['anomaly'] == -1]
offenders = anomalies['src_ip_code'].value_counts()
THRESHOLD = 3  # Adjust as needed
trigger_ips = offenders[offenders > THRESHOLD].index.tolist()

# Step 3: Simulate self-healing response
print("🚨 Triggered Self-Healing Response:")
if not trigger_ips:
    print("✅ No offending IPs exceeded threshold.")
else:
    for ip_code in trigger_ips:
        ip_str = src_ip_mapping.get(ip_code, f"[Unknown IP code {ip_code}]")
        print(f"🚫 Blocking IP: {ip_str} (Simulated IPTables or ACL)")
✅ Example Output You Should See
yaml
Copy
Edit
🚨 Triggered Self-Healing Response:
🚫 Blocking IP: 172.31.99.99 (Simulated IPTables or ACL)
🚫 Blocking IP: 10.100.200.1 (Simulated IPTables or ACL)
🚫 Blocking IP: 198.51.100.42 (Simulated IPTables or ACL)
🚫 Blocking IP: 10.246.3.107 (Simulated IPTables or ACL)
