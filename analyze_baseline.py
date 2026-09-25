import csv
import statistics

# ============================================================
# CYBERSHIELD-DT
# NORMAL BASELINE ANALYZER
# ============================================================

csv_path = r'C:\Users\anud9\baseline_data.csv'

data = {
    'Speed_kmh': [],
    'Acceleration_ms2': [],
    'Steering': [],
    'Throttle': [],
    'Brake': []
}


# ------------------------------------------------------------
# Read baseline data
# ------------------------------------------------------------

with open(csv_path, 'r') as file:

    reader = csv.DictReader(file)

    for row in reader:

        for parameter in data:

            data[parameter].append(
                float(row[parameter])
            )


print()
print("==============================================")
print("       CYBERSHIELD-DT BASELINE ANALYSIS")
print("==============================================")

print("Samples:", len(data['Speed_kmh']))
print()


# ------------------------------------------------------------
# Calculate statistics
# ------------------------------------------------------------

for parameter, values in data.items():

    minimum = min(values)
    maximum = max(values)
    average = statistics.mean(values)

    if len(values) > 1:
        std_dev = statistics.stdev(values)
    else:
        std_dev = 0.0

    print("----------------------------------------------")
    print(parameter)
    print(f"Minimum   : {minimum:.4f}")
    print(f"Maximum   : {maximum:.4f}")
    print(f"Average   : {average:.4f}")
    print(f"Std Dev   : {std_dev:.4f}")


print()
print("==============================================")
print("Baseline analysis completed.")
print("==============================================")