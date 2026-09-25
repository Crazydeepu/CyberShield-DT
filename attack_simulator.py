import carla
import time
import csv
import os
import math


# ============================================================
# CYBERSHIELD-DT
# SOFTWARE-BASED ATTACK SIMULATOR
# CARLA 0.9.16
# ============================================================

CSV_FILE = r"C:\Users\anud9\attack_telemetry.csv"


def get_speed_kmh(vehicle):
    velocity = vehicle.get_velocity()

    speed_ms = math.sqrt(
        velocity.x ** 2 +
        velocity.y ** 2 +
        velocity.z ** 2
    )

    return speed_ms * 3.6


def get_acceleration(vehicle):
    acceleration = vehicle.get_acceleration()

    return math.sqrt(
        acceleration.x ** 2 +
        acceleration.y ** 2 +
        acceleration.z ** 2
    )


def write_log(writer, vehicle, attack_type):
    transform = vehicle.get_transform()
    control = vehicle.get_control()

    speed = get_speed_kmh(vehicle)
    acceleration = get_acceleration(vehicle)

    writer.writerow([
        time.time(),
        vehicle.id,
        transform.location.x,
        transform.location.y,
        transform.location.z,
        speed,
        acceleration,
        control.steer,
        control.throttle,
        control.brake,
        attack_type
    ])


# ============================================================
# CONNECT TO CARLA
# ============================================================

print("=" * 55)
print("       CYBERSHIELD-DT ATTACK SIMULATOR")
print("=" * 55)

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()

print("Connected to CARLA")
print("Map:", world.get_map().name)


# ============================================================
# FIND EXISTING TESLA MODEL 3
# ============================================================

vehicle = None

for actor in world.get_actors():
    if actor.type_id == "vehicle.tesla.model3":
        vehicle = actor
        break


if vehicle is None:
    print()
    print("ERROR: Tesla Model 3 was not found.")
    print()
    print("Please start digital_twin.py first.")
    print("Keep the Digital Twin running and then start this script.")
    print()
    exit()


print()
print("Tesla Model 3 found")
print("Vehicle ID:", vehicle.id)


# ============================================================
# DISABLE AUTOPILOT
# ============================================================

vehicle.set_autopilot(False)

print("Autopilot disabled")
print()


# ============================================================
# CREATE ATTACK LOG
# ============================================================

file_exists = os.path.exists(CSV_FILE)

csv_file = open(
    CSV_FILE,
    "a",
    newline=""
)

writer = csv.writer(csv_file)

if not file_exists:

    writer.writerow([
        "Time",
        "Vehicle_ID",
        "X",
        "Y",
        "Z",
        "Speed_kmh",
        "Acceleration_ms2",
        "Steering",
        "Throttle",
        "Brake",
        "Attack_Type"
    ])


# ============================================================
# PHASE 1 — NORMAL OPERATION
# ============================================================

print("=" * 55)
print("PHASE 1: NORMAL VEHICLE BEHAVIOR")
print("=" * 55)

start_time = time.time()

while time.time() - start_time < 10:

    control = carla.VehicleControl()

    control.throttle = 0.35
    control.steer = 0.0
    control.brake = 0.0

    vehicle.apply_control(control)

    write_log(
        writer,
        vehicle,
        "NORMAL"
    )

    csv_file.flush()

    print(
        "NORMAL | Speed:",
        round(get_speed_kmh(vehicle), 2),
        "km/h"
    )

    time.sleep(0.5)


# ============================================================
# PHASE 2 — THROTTLE INJECTION ATTACK
# ============================================================

print()
print("=" * 55)
print("PHASE 2: THROTTLE INJECTION ATTACK")
print("=" * 55)

print("Simulating malicious throttle command...")

start_time = time.time()

while time.time() - start_time < 10:

    control = carla.VehicleControl()

    # Maliciously high throttle
    control.throttle = 0.95
    control.steer = 0.0
    control.brake = 0.0

    vehicle.apply_control(control)

    write_log(
        writer,
        vehicle,
        "THROTTLE_INJECTION"
    )

    csv_file.flush()

    print(
        "ATTACK: THROTTLE_INJECTION | Speed:",
        round(get_speed_kmh(vehicle), 2),
        "km/h"
    )

    time.sleep(0.5)


# ============================================================
# PHASE 3 — STEERING INJECTION ATTACK
# ============================================================

print()
print("=" * 55)
print("PHASE 3: STEERING INJECTION ATTACK")
print("=" * 55)

print("Simulating malicious steering commands...")

start_time = time.time()

while time.time() - start_time < 10:

    control = carla.VehicleControl()

    control.throttle = 0.35

    # Rapid alternating steering
    elapsed = time.time() - start_time

    if int(elapsed * 2) % 2 == 0:
        control.steer = 0.8
    else:
        control.steer = -0.8

    control.brake = 0.0

    vehicle.apply_control(control)

    write_log(
        writer,
        vehicle,
        "STEERING_INJECTION"
    )

    csv_file.flush()

    print(
        "ATTACK: STEERING_INJECTION | Steering:",
        round(control.steer, 2),
        "| Speed:",
        round(get_speed_kmh(vehicle), 2),
        "km/h"
    )

    time.sleep(0.5)


# ============================================================
# PHASE 4 — BRAKE INJECTION ATTACK
# ============================================================

print()
print("=" * 55)
print("PHASE 4: BRAKE INJECTION ATTACK")
print("=" * 55)

print("Simulating malicious braking command...")

start_time = time.time()

while time.time() - start_time < 8:

    control = carla.VehicleControl()

    control.throttle = 0.0
    control.steer = 0.0

    # Malicious brake command
    control.brake = 1.0

    vehicle.apply_control(control)

    write_log(
        writer,
        vehicle,
        "BRAKE_INJECTION"
    )

    csv_file.flush()

    print(
        "ATTACK: BRAKE_INJECTION | Speed:",
        round(get_speed_kmh(vehicle), 2),
        "km/h"
    )

    time.sleep(0.5)


# ============================================================
# PHASE 5 — RETURN TO SAFE STATE
# ============================================================

print()
print("=" * 55)
print("PHASE 5: SAFE STATE")
print("=" * 55)

control = carla.VehicleControl()

control.throttle = 0.0
control.steer = 0.0
control.brake = 1.0

vehicle.apply_control(control)

write_log(
    writer,
    vehicle,
    "SAFE_STATE"
)

csv_file.flush()

time.sleep(3)


# ============================================================
# CLOSE
# ============================================================

csv_file.close()

print()
print("=" * 55)
print("ATTACK SIMULATION COMPLETED")
print("=" * 55)

print()
print("Attack log saved to:")
print(CSV_FILE)

print()
print("Attack types generated:")
print("1. NORMAL")
print("2. THROTTLE_INJECTION")
print("3. STEERING_INJECTION")
print("4. BRAKE_INJECTION")

print()
print("Next step:")
print("Run anomaly_detector.py while testing these attacks.")
print("=" * 55)