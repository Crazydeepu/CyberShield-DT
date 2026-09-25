import carla
import time
import math
import csv
import statistics

# ============================================================
# CYBERSHIELD-DT
# REAL-TIME ANOMALY DETECTOR
# ============================================================

print("==============================================")
print("       CYBERSHIELD-DT ANOMALY DETECTOR")
print("==============================================")

# ------------------------------------------------------------
# 1. Connect to CARLA
# ------------------------------------------------------------

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()

print("Connected to CARLA")
print("Map:", world.get_map().name)


# ------------------------------------------------------------
# 2. Load baseline data
# ------------------------------------------------------------

baseline_file = r'C:\Users\anud9\baseline_data.csv'

baseline = {
    'Speed_kmh': [],
    'Acceleration_ms2': [],
    'Steering': [],
    'Throttle': [],
    'Brake': []
}

with open(baseline_file, 'r') as file:

    reader = csv.DictReader(file)

    for row in reader:

        for parameter in baseline:

            baseline[parameter].append(
                float(row[parameter])
            )


# ------------------------------------------------------------
# 3. Calculate baseline statistics
# ------------------------------------------------------------

mean_values = {}
std_values = {}

for parameter, values in baseline.items():

    mean_values[parameter] = statistics.mean(values)

    if len(values) > 1:
        std_values[parameter] = statistics.stdev(values)
    else:
        std_values[parameter] = 0.0


print()
print("Baseline loaded successfully")
print("Samples:", len(baseline['Speed_kmh']))

print()
print("Baseline statistics:")
print("----------------------------------------------")

for parameter in baseline:

    print(
        f"{parameter:20s} "
        f"Mean={mean_values[parameter]:.4f} "
        f"Std={std_values[parameter]:.4f}"
    )


# ------------------------------------------------------------
# 4. Find vehicle
# ------------------------------------------------------------

vehicles = world.get_actors().filter(
    'vehicle.tesla.model3'
)

if len(vehicles) == 0:

    print()
    print("No Tesla Model 3 found.")
    print("Please run the Digital Twin first.")

    exit()


vehicle = vehicles[0]

print()
print("Vehicle found")
print("Vehicle ID:", vehicle.id)


# ------------------------------------------------------------
# 5. Start anomaly detection
# ------------------------------------------------------------

print()
print("==============================================")
print("REAL-TIME ANOMALY DETECTION STARTED")
print("==============================================")
print()
print("Press Ctrl+C to stop.")
print()


# ------------------------------------------------------------
# 6. Detection loop
# ------------------------------------------------------------

try:

    while True:

        # ----------------------------------------------------
        # Vehicle velocity
        # ----------------------------------------------------

        velocity = vehicle.get_velocity()

        speed_ms = math.sqrt(
            velocity.x ** 2 +
            velocity.y ** 2 +
            velocity.z ** 2
        )

        speed_kmh = speed_ms * 3.6


        # ----------------------------------------------------
        # Vehicle acceleration
        # ----------------------------------------------------

        acceleration = vehicle.get_acceleration()

        acceleration_ms2 = math.sqrt(
            acceleration.x ** 2 +
            acceleration.y ** 2 +
            acceleration.z ** 2
        )


        # ----------------------------------------------------
        # Vehicle controls
        # ----------------------------------------------------

        control = vehicle.get_control()

        steering = control.steer
        throttle = control.throttle
        brake = control.brake


        current_values = {

            'Speed_kmh': speed_kmh,

            'Acceleration_ms2': acceleration_ms2,

            'Steering': steering,

            'Throttle': throttle,

            'Brake': brake
        }


        # ----------------------------------------------------
        # Calculate anomaly scores
        # ----------------------------------------------------

        anomaly_scores = {}

        for parameter, value in current_values.items():

            mean = mean_values[parameter]

            std = std_values[parameter]

            if std > 0:

                z_score = abs(
                    (value - mean) / std
                )

            else:

                z_score = 0.0


            anomaly_scores[parameter] = z_score


        # ----------------------------------------------------
        # Determine overall status
        # ----------------------------------------------------

        anomalous_parameters = []

        for parameter, score in anomaly_scores.items():

            if score >= 3.0:

                anomalous_parameters.append(parameter)


        if len(anomalous_parameters) >= 2:

            status = "ANOMALY DETECTED"

        else:

            status = "NORMAL"


        # ----------------------------------------------------
        # Print result
        # ----------------------------------------------------

        print("----------------------------------------------")

        print(
            f"Speed        : {speed_kmh:6.2f} km/h"
        )

        print(
            f"Acceleration : {acceleration_ms2:6.2f} m/s2"
        )

        print(
            f"Steering     : {steering:6.2f}"
        )

        print(
            f"Throttle     : {throttle:6.2f}"
        )

        print(
            f"Brake        : {brake:6.2f}"
        )

        print()

        print("Anomaly Scores:")

        for parameter, score in anomaly_scores.items():

            print(
                f"{parameter:20s}: {score:.2f}"
            )

        print()

        if status == "NORMAL":

            print("STATUS: 🟢 NORMAL")

        else:

            print("STATUS: 🔴 ANOMALY DETECTED")

            print(
                "Affected parameters:",
                anomalous_parameters
            )

        print("----------------------------------------------")


        time.sleep(0.5)


except KeyboardInterrupt:

    print()
    print("Stopping anomaly detector...")

    print("Detection stopped.")