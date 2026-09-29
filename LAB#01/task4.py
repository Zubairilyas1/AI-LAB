# Task 4: Smart Agriculture Field Monitoring (Beginner Version)
# AI-2002 Lab

import numpy as np

# ---------- Data ----------
field_data = [
    {
        "field": "F1",
        "temperature": 34,
        "humidity": 55,
        "soil_moisture": 28
    },
    {
        "field": "F2",
        "temperature": 29,
        "humidity": 72,
        "soil_moisture": 61
    },
    {
        "field": "F3",
        "temperature": 38,
        "humidity": 48,
        "soil_moisture": 22
    },
    {
        "field": "F4",
        "temperature": 31,
        "humidity": 65,
        "soil_moisture": 47
    },
    {
        "field": "F5",
        "temperature": 36,
        "humidity": 50,
        "soil_moisture": 30
    }
]

print("=== Field Data Loaded ===")
for field in field_data:
    print("Field:", field["field"], 
          "Temp:", field["temperature"], 
          "Humidity:", field["humidity"], 
          "Soil Moisture:", field["soil_moisture"])
print("\n")

# ---------- 1. Identify fields requiring irrigation (soil_moisture < 30) ----------
print("--- Fields Requiring Irrigation (Soil Moisture < 30) ---")
irrigation_fields = []

for field in field_data:
    if field["soil_moisture"] < 30:
        print("Field:", field["field"], 
              "Soil Moisture:", field["soil_moisture"])
        irrigation_fields.append(field["field"])

if len(irrigation_fields) == 0:
    print("No fields require irrigation.")

print("\n")

# ---------- 2. Identify fields experiencing heat stress (temperature > 35) ----------
print("--- Fields Experiencing Heat Stress (Temperature > 35) ---")
heat_stress_fields = []

for field in field_data:
    if field["temperature"] > 35:
        print("Field:", field["field"], 
              "Temperature:", field["temperature"])
        heat_stress_fields.append(field["field"])

if len(heat_stress_fields) == 0:
    print("No fields experiencing heat stress.")

print("\n")

# ---------- 3. Identify fields satisfying both conditions ----------
print("--- Fields with BOTH Irrigation AND Heat Stress ---")
both_conditions = []

for field in field_data:
    if field["soil_moisture"] < 30 and field["temperature"] > 35:
        print("Field:", field["field"], 
              "Soil Moisture:", field["soil_moisture"], 
              "Temperature:", field["temperature"])
        both_conditions.append(field["field"])

if len(both_conditions) == 0:
    print("No fields satisfy both conditions.")

print("\n")

# ---------- 4. Convert data to NumPy matrix ----------
# Rows = fields, Columns = temperature, humidity, soil_moisture
sensor_matrix = []

for field in field_data:
    row = [
        field["temperature"],
        field["humidity"],
        field["soil_moisture"]
    ]
    sensor_matrix.append(row)

# Convert to NumPy array
sensor_matrix = np.array(sensor_matrix)

print("--- NumPy Sensor Matrix ---")
print("Rows = Fields (F1-F5), Columns = [Temperature, Humidity, Soil Moisture]")
print(sensor_matrix)
print("\n")

# ---------- 5. Calculate means ----------
print("--- Mean Values ---")
mean_temp = np.mean(sensor_matrix[:, 0])  # Column 0: temperature
mean_humidity = np.mean(sensor_matrix[:, 1])  # Column 1: humidity
mean_soil = np.mean(sensor_matrix[:, 2])  # Column 2: soil_moisture

print("Mean Temperature:", round(mean_temp, 2))
print("Mean Humidity:", round(mean_humidity, 2))
print("Mean Soil Moisture:", round(mean_soil, 2))
print("\n")

# ---------- 6. Calculate variance ----------
print("--- Variance Values ---")
var_temp = np.var(sensor_matrix[:, 0])
var_humidity = np.var(sensor_matrix[:, 1])
var_soil = np.var(sensor_matrix[:, 2])

print("Variance of Temperature:", round(var_temp, 2))
print("Variance of Humidity:", round(var_humidity, 2))
print("Variance of Soil Moisture:", round(var_soil, 2))
print("\n")

# ---------- 7. Identify sensor with highest variance ----------
# Store variances in a dictionary
variances = {
    "Temperature": var_temp,
    "Humidity": var_humidity,
    "Soil Moisture": var_soil
}

# Find the key with the maximum value
highest_var_sensor = max(variances, key=variances.get)
highest_var_value = variances[highest_var_sensor]

print("--- Sensor with Highest Variance ---")
print("Sensor:", highest_var_sensor)
print("Variance:", round(highest_var_value, 2))
print("\n")

# ---------- 8. Calculate field-risk score ----------
# Step 8a: Normalize each column (Min-Max normalization)
print("--- Normalization ---")
col_mins = np.min(sensor_matrix, axis=0)
col_maxs = np.max(sensor_matrix, axis=0)

normalized_data = (sensor_matrix - col_mins) / (col_maxs - col_mins)

print("Normalized data (0 to 1):")
print(normalized_data)
print("\n")

# Step 8b: Calculate risk scores
# Risk Score = 0.4 × norm_temp + 0.2 × norm_humidity + 0.4 × (1 - norm_soil)
print("--- Risk Scores ---")
risk_scores = []

for i in range(len(normalized_data)):
    norm_temp = normalized_data[i][0]
    norm_humidity = normalized_data[i][1]
    norm_soil = normalized_data[i][2]
    
    risk_score = (0.4 * norm_temp) + (0.2 * norm_humidity) + (0.4 * (1 - norm_soil))
    risk_scores.append(risk_score)
    
    field_name = field_data[i]["field"]
    print("Field", field_name, "→ Risk Score:", round(risk_score, 4))

print("\n")

# ---------- 9. Rank fields from highest to lowest risk ----------
# Create a list of (field_name, risk_score) pairs
field_risk_pairs = []

for i in range(len(field_data)):
    field_name = field_data[i]["field"]
    risk_score = risk_scores[i]
    field_risk_pairs.append((field_name, risk_score))

# Sort by risk score (highest first) using a lambda function
ranked_fields = sorted(field_risk_pairs, key=lambda x: x[1], reverse=True)

print("--- Fields Ranked by Risk (Highest to Lowest) ---")
print("Position | Field | Risk Score")
print("-" * 40)
for position, (field, score) in enumerate(ranked_fields, start=1):
    print(position, "      |", field, " |", round(score, 4))
print("\n")

# ---------- 10. Display recommendations ----------
print("--- Recommendations ---")

for field, score in ranked_fields:
    if score > 0.6:
        risk_level = "HIGH RISK → Immediate inspection required"
    elif score > 0.4:
        risk_level = "MEDIUM RISK → Monitor field"
    else:
        risk_level = "LOW RISK → Normal condition"
    
    print("Field", field, "| Score:", round(score, 4), "→", risk_level)

print("\n")

# ---------- Extra: Display summary of all fields ----------
print("="*60)
print("           AGRICULTURE FIELD MONITORING REPORT")
print("="*60)

print("\n--- Field Status Summary ---")
for field in field_data:
    field_name = field["field"]
    temp = field["temperature"]
    humidity = field["humidity"]
    soil = field["soil_moisture"]
    
    # Check conditions for this field
    needs_irrigation = soil < 30
    has_heat_stress = temp > 35
    
    status = []
    if needs_irrigation:
        status.append("Needs Irrigation")
    if has_heat_stress:
        status.append("Heat Stress")
    if not needs_irrigation and not has_heat_stress:
        status.append("Normal")
    
    print("Field", field_name, "|", ", ".join(status))

print("\n--- Summary Statistics ---")
print("Mean Temperature:", round(mean_temp, 2))
print("Mean Humidity:", round(mean_humidity, 2))
print("Mean Soil Moisture:", round(mean_soil, 2))
print("\nHighest Variance Sensor:", highest_var_sensor)

print("\n--- Risk Classification Summary ---")
high_risk = 0
medium_risk = 0
low_risk = 0

for field, score in ranked_fields:
    if score > 0.6:
        high_risk = high_risk + 1
    elif score > 0.4:
        medium_risk = medium_risk + 1
    else:
        low_risk = low_risk + 1

print("High Risk Fields:", high_risk)
print("Medium Risk Fields:", medium_risk)
print("Low Risk Fields:", low_risk)

print("\n" + "="*60)
print("            END OF REPORT")
print("="*60)