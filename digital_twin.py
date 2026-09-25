import carla
import time
import math
import csv

# ============================================================
# CYBERSHIELD-DT
# Digital Twin for Autonomous Vehicle
# CARLA 0.9.16
# ============================================================

# ------------------------------------------------------------
# 1. Connect to CARLA
# ------------------------------------------------------------

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

world = client.get_world()

print("Connected to CARLA")


# ------------------------------------------------------------
# 2. Get vehicle blueprint
# ------------------------------------------------------------

blueprint_library = world.get_blueprint_library()

vehicle_bp = blueprint_library.filter(
    'vehicle.tesla.model3'
)[0]


# ------------------------------------------------------------
# 3. Select spawn point
# ------------------------------------------------------------

spawn_points = world.get_map().get_spawn_points()

spawn_point = spawn_points[0]


# ------------------------------------------------------------
# 4. Spawn vehicle
# ------------------------------------------------------------

vehicle = world.try_spawn_actor(
    vehicle_bp,
    spawn_point
)

if vehicle is None:
    print("ERROR: Could not spawn vehicle")
    exit()

print("Vehicle spawned successfully")
print("Vehicle ID:", vehicle.id)


# ------------------------------------------------------------
# 5. Enable autopilot
# ------------------------------------------------------------

vehicle.set_autopilot(True)

print("Autopilot enabled")
print("Digital Twin started")
print("---------------------------------------------")


# ------------------------------------------------------------
# 6. Get spectator camera
# ------------------------------------------------------------

spectator = world.get_spectator()


# ------------------------------------------------------------
# 7. Create CSV telemetry file
# ------------------------------------------------------------

csv_file = open(
    r'C:\Users\anud9\digital_twin_telemetry.csv',
    'w',
    newline=''
)

csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    'Time',
    'Vehicle_ID',
    'X',
    'Y',
    'Z',
    'Speed_kmh',
    'Acceleration_ms2',
    'Steering',
    'Throttle',
    'Brake',
    'Cyber_Status'
])


# ------------------------------------------------------------
# 8. Digital Twin loop
# ------------------------------------------------------------

try:

    while True:

        # ----------------------------------------------------
        # Get vehicle transform
        # ----------------------------------------------------

        vehicle_transform = vehicle.get_transform()

        location = vehicle_transform.location

        rotation = vehicle_transform.rotation


        # ----------------------------------------------------
        # Get velocity
        # ----------------------------------------------------

        velocity = vehicle.get_velocity()

        speed_ms = math.sqrt(
            velocity.x ** 2 +
            velocity.y ** 2 +
            velocity.z ** 2
        )

        speed_kmh = speed_ms * 3.6


        # ----------------------------------------------------
        # Get acceleration
        # ----------------------------------------------------

        acceleration = vehicle.get_acceleration()

        acceleration_ms2 = math.sqrt(
            acceleration.x ** 2 +
            acceleration.y ** 2 +
            acceleration.z ** 2
        )


        # ----------------------------------------------------
        # Get vehicle controls
        # ----------------------------------------------------

        control = vehicle.get_control()

        steering = control.steer
        throttle = control.throttle
        brake = control.brake


        # ----------------------------------------------------
        # Digital Twin state
        # ----------------------------------------------------

        digital_twin = {

            'vehicle_id': vehicle.id,

            'position': (
                location.x,
                location.y,
                location.z
            ),

            'speed': speed_kmh,

            'acceleration': acceleration_ms2,

            'steering': steering,

            'throttle': throttle,

            'brake': brake,

            'cyber_status': 'NORMAL'
        }


        # ----------------------------------------------------
        # Move CARLA spectator camera
        # ----------------------------------------------------

        camera_location = vehicle_transform.transform(
            carla.Location(
                x=-8.0,
                z=4.0
            )
        )

        camera_rotation = carla.Rotation(
            pitch=-15.0,
            yaw=rotation.yaw,
            roll=0.0
        )

        spectator.set_transform(
            carla.Transform(
                camera_location,
                camera_rotation
            )
        )


        # ----------------------------------------------------
        # Digital Twin text
        # ----------------------------------------------------

        text = (
            "DIGITAL TWIN\n"
            "--------------------\n"
            f"Vehicle ID: {vehicle.id}\n"
            f"Speed: {speed_kmh:.1f} km/h\n"
            f"Acceleration: {acceleration_ms2:.2f} m/s2\n"
            f"Steering: {steering:.2f}\n"
            f"Throttle: {throttle:.2f}\n"
            f"Brake: {brake:.2f}\n"
            "Cyber Status: NORMAL"
        )


        # ----------------------------------------------------
        # Draw Digital Twin information above vehicle
        # ----------------------------------------------------

        text_location = carla.Location(
            x=location.x,
            y=location.y,
            z=location.z + 3.0
        )

        world.debug.draw_string(
            text_location,
            text,
            draw_shadow=True,
            life_time=0.6
        )


        # ----------------------------------------------------
        # Print Digital Twin information in terminal
        # ----------------------------------------------------

        print("\n========== DIGITAL TWIN ==========")

        print(
            f"Vehicle ID     : {vehicle.id}"
        )

        print(
            f"Position       : "
            f"X={location.x:.2f}, "
            f"Y={location.y:.2f}, "
            f"Z={location.z:.2f}"
        )

        print(
            f"Speed          : "
            f"{speed_kmh:.2f} km/h"
        )

        print(
            f"Acceleration   : "
            f"{acceleration_ms2:.2f} m/s2"
        )

        print(
            f"Steering       : "
            f"{steering:.2f}"
        )

        print(
            f"Throttle       : "
            f"{throttle:.2f}"
        )

        print(
            f"Brake          : "
            f"{brake:.2f}"
        )

        print(
            f"Cyber Status   : "
            f"{digital_twin['cyber_status']}"
        )

        print("===================================")


        # ----------------------------------------------------
        # Save telemetry to CSV
        # ----------------------------------------------------

        csv_writer.writerow([
            time.time(),
            vehicle.id,
            location.x,
            location.y,
            location.z,
            speed_kmh,
            acceleration_ms2,
            steering,
            throttle,
            brake,
            digital_twin['cyber_status']
        ])

        csv_file.flush()


        # ----------------------------------------------------
        # Update interval
        # ----------------------------------------------------

        time.sleep(0.5)


# ------------------------------------------------------------
# 9. Stop with Ctrl+C
# ------------------------------------------------------------

except KeyboardInterrupt:

    print("\nStopping Digital Twin...")


# ------------------------------------------------------------
# 10. Clean up
# ------------------------------------------------------------

finally:

    csv_file.close()

    vehicle.set_autopilot(False)

    vehicle.destroy()

    print("Vehicle destroyed")
    print("Digital Twin stopped")