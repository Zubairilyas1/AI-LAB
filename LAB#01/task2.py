# Task 2: Cybersecurity Login Risk Analyzer (Beginner Version)
# AI-2002 Lab

from functools import reduce   # we need this for reduce()

# ---------- Data ----------
login_data = {
    "192.168.1.10": 3,
    "192.168.1.21": 17,
    "192.168.1.35": 5,
    "192.168.1.42": 24,
    "192.168.1.51": 11,
    "192.168.1.63": 2
}

print("=== Login Data Loaded ===")
for ip, attempts in login_data.items():
    print("IP:", ip, "Failed Attempts:", attempts)

print("\n" + "="*50 + "\n")   # separator line

# ---------- 1. Identify suspicious IPs using filter() and lambda ----------
# A lambda function checks if attempts > 10
suspicious_ips_data = filter(lambda item: item[1] > 10, login_data.items())

# Convert to a list so we can use it multiple times
suspicious_list = list(suspicious_ips_data)

print("--- Suspicious IPs (more than 10 failed attempts) ---")
if len(suspicious_list) == 0:
    print("No suspicious IPs found.")
else:
    for ip, attempts in suspicious_list:
        print("IP:", ip, "Failed Attempts:", attempts)

print("\n")

# ---------- 2. & 3. Calculate risk scores using map() ----------
# Risk Score = Failed Attempts × 2
risk_scores = map(lambda item: (item[0], item[1] * 2), suspicious_list)

# Convert to list so we can use it
risk_list = list(risk_scores)

print("--- Risk Scores (Failed Attempts × 2) ---")
if len(risk_list) > 0:
    for ip, risk in risk_list:
        print("IP:", ip, "Risk Score:", risk)
else:
    print("No risk scores to display.")

print("\n")

# ---------- 4. Calculate total risk score using reduce() ----------
if len(risk_list) > 0:
    # Extract just the risk scores from the list of tuples
    risk_values = []
    for ip, risk in risk_list:
        risk_values.append(risk)
    
    # Add all risk scores together
    total_risk = reduce(lambda x, y: x + y, risk_values)
    print("Total Risk Score (sum of all risk scores):", total_risk)
else:
    print("Total Risk Score: 0 (No suspicious IPs)")

print("\n")

# ---------- 5. Store suspicious IPs in a set ----------
suspicious_ips_set = set()
for ip, attempts in suspicious_list:
    suspicious_ips_set.add(ip)

print("--- Suspicious IPs (stored in a set) ---")
print(suspicious_ips_set)

print("\n")

# ---------- 6. Display IP with the highest failed attempts ----------
if len(suspicious_list) > 0:
    # Find the IP with maximum attempts
    max_attempts = 0
    max_ip = ""
    
    for ip, attempts in suspicious_list:
        if attempts > max_attempts:
            max_attempts = attempts
            max_ip = ip
    
    print("--- IP with the highest failed attempts ---")
    print("IP:", max_ip, "Failed Attempts:", max_attempts)
else:
    print("No suspicious IPs to analyze.")

print("\n")

# ---------- 7. Classify each suspicious IP ----------
print("--- Risk Classification ---")
if len(suspicious_list) > 0:
    for ip, attempts in suspicious_list:
        if attempts >= 11 and attempts <= 15:
            risk_level = "Medium Risk"
        elif attempts >= 16 and attempts <= 20:
            risk_level = "High Risk"
        else:   # above 20
            risk_level = "Critical Risk"
        
        print("IP:", ip, "Attempts:", attempts, "→", risk_level)
else:
    print("No suspicious IPs to classify.")

print("\n")

# ---------- 8. Final Security Report ----------
print("="*50)
print("               FINAL SECURITY REPORT")
print("="*50)

if len(suspicious_list) > 0:
    print("Total suspicious IPs detected:", len(suspicious_list))
    print("Suspicious IP addresses:", suspicious_ips_set)
    
    # Display classification summary
    medium_count = 0
    high_count = 0
    critical_count = 0
    
    for ip, attempts in suspicious_list:
        if attempts >= 11 and attempts <= 15:
            medium_count = medium_count + 1
        elif attempts >= 16 and attempts <= 20:
            high_count = high_count + 1
        else:
            critical_count = critical_count + 1
    
    print("\n--- Risk Level Summary ---")
    print("Medium Risk (11-15 attempts):", medium_count)
    print("High Risk (16-20 attempts):", high_count)
    print("Critical Risk (above 20):", critical_count)
    
    print("\n--- IP with Highest Failed Attempts ---")
    print("IP:", max_ip, "| Attempts:", max_attempts)
    
else:
    print("✓ No suspicious activity detected.")
    print("✓ All IP addresses have 10 or fewer failed attempts.")

print("\n" + "="*50)
print("            END OF REPORT")
print("="*50)