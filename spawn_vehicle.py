import carla
import random
import time

# Connect to CARLA
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the current world
world = client.get_world()

# Get vehicle blueprints
blueprint_library = world.get_blueprint_library()

vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]

# Get available spawn points
spawn_points = world.get_map().get_spawn_points()

# Select a random spawn point
spawn_point = random.choice(spawn_points)

# Spawn vehicle
vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

if vehicle is not None:
    print("Vehicle spawned successfully")
    print("Vehicle ID:", vehicle.id)
else:
    print("Vehicle could not be spawned")

# Keep vehicle in the simulation for 10 seconds
time.sleep(10)

# Destroy vehicle
if vehicle is not None:
    vehicle.destroy()
    print("Vehicle destroyed")