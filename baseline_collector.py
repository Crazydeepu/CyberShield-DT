import carla
import time
import math
import csv
import random

# ============================================================
# CYBERSHIELD-DT
# NORMAL VEHICLE BEHAVIOR BASELINE COLLECTOR
# CARLA 0.9.16
# ============================================================

print("Connecting to CARLA...")

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()

print("Connected to CARLA")
print("Map:", world.get_map().name)


# ------------------------------------------------------------
# 1. Get vehicle blueprint
# ------------------------------------------------------------

blueprint_library = world.get_blueprint_library()

vehicle_bp = blueprint_library.filter(
    'vehicle.tesla.model3'
)[0]


# ------------------------------------------------------------
# 2. Find a spawn point
# ------------------------------------------------------------

spawn_points = world.get_map().get_spawn_points()

random.shuffle(spawn_points)

vehicle = None

for spawn_point in spawn_points:
    vehicle = world.try_spawn_actor(
        vehicle_bp,
        spawn_point
    )

    if vehicle is not None:
        break


if vehicle is None:
    print("ERROR: Could not spawn vehicle")
    exit()


print("Vehicle spawned successfully")
print("Vehicle ID:", vehicle.id)


# ------------------------------------------------------------
# 3. Enable autopilot
# ------------------------------------------------------------

vehicle.set_autopilot(True)

print("Autopilot enabled")
print("Collecting NORMAL vehicle behavior...")
print("Collection time: 120 seconds")
print("--------------------------------------------")


# ------------------------------------------------------------
# 4. Create CSV file
# ------------------------------------------------------------

csv_path = r'C:\Users\anud9\baseline_data.csv'

csv_file = open(
    csv_path,
    'w',
    newline=''
)

writer = csv.writer(csv_file)

writer.writerow([
    'Time',
    'Vehicle_ID',
    'X',
    'Y',
    'Z',
    'Speed_kmh',
    'Acceleration_ms2',
    'Steering',
    'Throttle',
    'Brake'
])


# ------------------------------------------------------------
# 5. Collect normal behavior
# ------------------------------------------------------------

start_time = time.time()

sample_count = 0

try:

    while time.time() - start_time < 120:

        # --------------------------------------------
        # Vehicle position
        # --------------------------------------------

        location = vehicle.get_location()


        # --------------------------------------------
        # Vehicle velocity
        # --------------------------------------------

        velocity = vehicle.get_velocity()

        speed_ms = math.sqrt(
            velocity.x ** 2 +
            velocity.y ** 2 +
            velocity.z ** 2
        )

        speed_kmh = speed_ms * 3.6


        # --------------------------------------------
        # Vehicle acceleration
        # --------------------------------------------

        acceleration = vehicle.get_acceleration()

        acceleration_ms2 = math.sqrt(
            acceleration.x ** 2 +
            acceleration.y ** 2 +
            acceleration.z ** 2
        )


        # --------------------------------------------
        # Vehicle controls
        # --------------------------------------------

        control = vehicle.get_control()

        steering = control.steer
        throttle = control.throttle
        brake = control.brake


        # --------------------------------------------
        # Save data
        # --------------------------------------------

        writer.writerow([
            time.time(),
            vehicle.id,
            location.x,
            location.y,
            location.z,
            speed_kmh,
            acceleration_ms2,
            steering,
            throttle,
            brake
        ])

        csv_file.flush()

        sample_count += 1


        # --------------------------------------------
        # Console output
        # --------------------------------------------

        print(
            f"Sample: {sample_count:4d} | "
            f"Speed: {speed_kmh:6.2f} km/h | "
            f"Acceleration: {acceleration_ms2:5.2f} m/s2 | "
            f"Steering: {steering:5.2f} | "
            f"Throttle: {throttle:5.2f} | "
            f"Brake: {brake:5.2f}"
        )


        # Collect every 0.5 seconds
        time.sleep(0.5)


except KeyboardInterrupt:

    print("\nCollection stopped manually.")


finally:

    csv_file.close()

    vehicle.set_autopilot(False)

    vehicle.destroy()

    print("--------------------------------------------")
    print("NORMAL baseline collection completed.")
    print("Samples collected:", sample_count)
    print("Saved to:", csv_path)
    print("Vehicle destroyed.")