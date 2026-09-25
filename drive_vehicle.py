import carla
import time

print("======================================")
print("     CYBERSHIELD-DT VEHICLE DRIVER")
print("======================================")

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()

vehicle = None

# Find the Tesla Model 3 used by our Digital Twin
for actor in world.get_actors():
    if actor.type_id == "vehicle.tesla.model3":
        vehicle = actor
        break

if vehicle is None:
    print("ERROR: Tesla Model 3 not found.")
    print("Start digital_twin.py first.")
    exit()

print("Vehicle found!")
print("Vehicle ID:", vehicle.id)

# Disable autopilot so we control the vehicle directly
vehicle.set_autopilot(False)

print("Starting controlled driving...")
print("Press CTRL+C to stop.")

try:
    while True:

        # Forward driving
        control = carla.VehicleControl()
        control.throttle = 0.35
        control.steer = 0.0
        control.brake = 0.0

        vehicle.apply_control(control)

        time.sleep(2)

        # Small steering change
        control.throttle = 0.30
        control.steer = 0.08
        control.brake = 0.0

        vehicle.apply_control(control)

        time.sleep(2)

        # Straight driving again
        control.throttle = 0.35
        control.steer = 0.0
        control.brake = 0.0

        vehicle.apply_control(control)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping vehicle...")

    control = carla.VehicleControl()
    control.throttle = 0.0
    control.steer = 0.0
    control.brake = 1.0

    vehicle.apply_control(control)

    print("Vehicle stopped.")