# ============================================================
# CyberShield-DT
# Manual / Autonomous Controller + Cybersecurity Attack
# CARLA 0.9.16
#
# Controls:
# W / UP       -> Forward
# S / DOWN     -> Brake
# A / LEFT     -> Steer Left
# D / RIGHT    -> Steer Right
# X            -> Reverse
# T            -> Toggle Manual / Autonomous
# F            -> Toggle Throttle Injection Attack
# SPACE        -> Emergency Brake
# R            -> Reset Steering
# ESC          -> Exit
# ============================================================

import carla
import pygame
import math
import time
import csv
import os


# ============================================================
# SETTINGS
# ============================================================

WIDTH = 1000
HEIGHT = 650

NORMAL_THROTTLE = 0.45
ATTACK_THROTTLE = 0.90
REVERSE_THROTTLE = 0.40
NORMAL_BRAKE = 0.60
STEER_AMOUNT = 0.50

TELEMETRY_FILE = r"C:\Users\anud9\cybershield_live_telemetry.csv"


# ============================================================
# CONNECT TO CARLA
# ============================================================

print("===================================================")
print("CyberShield-DT Manual / Autonomous Controller")
print("===================================================")

print("\nConnecting to CARLA...")

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)

world = client.get_world()

print("Connected to CARLA")
print("Map:", world.get_map().name)


# ============================================================
# FIND TESLA MODEL 3
# ============================================================

vehicle = None

for actor in world.get_actors():

    if actor.type_id == "vehicle.tesla.model3":

        vehicle = actor
        break


if vehicle is None:

    print("\nERROR: Tesla Model 3 was not found.")
    print("Please start digital_twin.py first.")

    raise SystemExit


print("Vehicle found.")
print("Vehicle ID:", vehicle.id)


# ============================================================
# START IN MANUAL MODE
# ============================================================

manual_mode = True

vehicle.set_autopilot(False)


# ============================================================
# INITIALIZE PYGAME
# ============================================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "CyberShield-DT - Autonomous Vehicle Cybersecurity"
)

clock = pygame.time.Clock()


# ============================================================
# FONTS
# ============================================================

font_title = pygame.font.SysFont(
    "Arial",
    24
)

font_main = pygame.font.SysFont(
    "Arial",
    18
)

font_small = pygame.font.SysFont(
    "Arial",
    16
)


# ============================================================
# CAMERA
# ============================================================

blueprint_library = world.get_blueprint_library()

camera_bp = blueprint_library.find(
    "sensor.camera.rgb"
)

camera_bp.set_attribute(
    "image_size_x",
    str(WIDTH)
)

camera_bp.set_attribute(
    "image_size_y",
    str(HEIGHT)
)

camera_bp.set_attribute(
    "fov",
    "90"
)


camera_transform = carla.Transform(

    carla.Location(
        x=-7.0,
        y=0.0,
        z=3.0
    ),

    carla.Rotation(
        pitch=-15.0,
        yaw=0.0,
        roll=0.0
    )
)


camera = world.spawn_actor(

    camera_bp,

    camera_transform,

    attach_to=vehicle
)


print("Camera attached successfully.")


# ============================================================
# CAMERA IMAGE
# ============================================================

latest_image = None


def process_camera(image):

    global latest_image

    latest_image = image


camera.listen(
    process_camera
)


# ============================================================
# VEHICLE CONTROL
# ============================================================

control = carla.VehicleControl()

control.throttle = 0.0
control.brake = 0.0
control.steer = 0.0
control.reverse = False


# ============================================================
# CYBERSECURITY VARIABLES
# ============================================================

attack_active = False

attack_type = "NONE"

requested_throttle = 0.0

applied_throttle = 0.0


# ============================================================
# TELEMETRY FILE
# ============================================================

telemetry_folder = os.path.dirname(
    TELEMETRY_FILE
)

if telemetry_folder:

    os.makedirs(
        telemetry_folder,
        exist_ok=True
    )


csv_file = open(
    TELEMETRY_FILE,
    "w",
    newline=""
)

csv_writer = csv.writer(
    csv_file
)


csv_writer.writerow([

    "Timestamp",
    "Vehicle_ID",

    "X",
    "Y",
    "Z",

    "Speed_kmh",

    "Acceleration_ms2",

    "Steering",

    "Requested_Throttle",

    "Applied_Throttle",

    "Brake",

    "Reverse",

    "Manual_Mode",

    "Attack_Active",

    "Attack_Type"

])


# ============================================================
# SPEED
# ============================================================

def get_speed():

    velocity = vehicle.get_velocity()

    speed = math.sqrt(

        velocity.x ** 2
        +
        velocity.y ** 2
        +
        velocity.z ** 2

    )

    return speed * 3.6


# ============================================================
# ACCELERATION
# ============================================================

def get_acceleration():

    acceleration = vehicle.get_acceleration()

    value = math.sqrt(

        acceleration.x ** 2
        +
        acceleration.y ** 2
        +
        acceleration.z ** 2

    )

    return value


# ============================================================
# CONTROLS INFORMATION
# ============================================================

print("\n===================================================")
print("CONTROLS")
print("===================================================")

print("W / UP       : Forward")
print("S / DOWN     : Brake")
print("A / LEFT     : Steer Left")
print("D / RIGHT    : Steer Right")
print("X            : Reverse")
print("T            : Manual / Autonomous")
print("F            : Throttle Injection")
print("SPACE        : Emergency Brake")
print("R            : Reset Steering")
print("ESC          : Exit")

print("===================================================\n")


# ============================================================
# MAIN LOOP
# ============================================================

running = True


try:

    while running:

        # ====================================================
        # DISPLAY CAMERA
        # ====================================================

        if latest_image is not None:

            try:

                image = pygame.image.frombuffer(

                    latest_image.raw_data,

                    (
                        latest_image.width,
                        latest_image.height
                    ),

                    "BGRA"

                )

                screen.blit(
                    image,
                    (0, 0)
                )

            except Exception as camera_error:

                print(
                    "Camera display error:",
                    camera_error
                )


        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            if event.type == pygame.KEYDOWN:

                # --------------------------------------------
                # ESC
                # --------------------------------------------

                if event.key == pygame.K_ESCAPE:

                    running = False


                # --------------------------------------------
                # MANUAL / AUTONOMOUS TOGGLE
                # --------------------------------------------

                elif event.key == pygame.K_t:

                    manual_mode = not manual_mode


                    if manual_mode:

                        # ------------------------------------
                        # SWITCH TO MANUAL
                        # ------------------------------------

                        vehicle.set_autopilot(False)

                        control.throttle = 0.0
                        control.brake = 0.0
                        control.steer = 0.0
                        control.reverse = False

                        print(
                            "\n"
                            "========================================"
                        )

                        print(
                            "MODE: MANUAL"
                        )

                        print(
                            "Driver control enabled."
                        )

                        print(
                            "========================================"
                        )


                    else:

                        # ------------------------------------
                        # SWITCH TO AUTONOMOUS
                        # ------------------------------------

                        attack_active = False
                        attack_type = "NONE"

                        control.throttle = 0.0
                        control.brake = 0.0
                        control.steer = 0.0
                        control.reverse = False

                        vehicle.set_autopilot(True)

                        print(
                            "\n"
                            "========================================"
                        )

                        print(
                            "MODE: AUTONOMOUS"
                        )

                        print(
                            "CARLA autopilot enabled."
                        )

                        print(
                            "========================================"
                        )


                # --------------------------------------------
                # THROTTLE INJECTION
                # --------------------------------------------

                elif event.key == pygame.K_f:

                    if not manual_mode:

                        print(
                            "\nThrottle injection requires "
                            "MANUAL mode."
                        )

                    else:

                        attack_active = not attack_active


                        if attack_active:

                            attack_type = (
                                "THROTTLE INJECTION"
                            )

                            print(
                                "\n"
                                "========================================"
                            )

                            print(
                                "CYBER ATTACK ACTIVATED"
                            )

                            print(
                                "Attack: THROTTLE INJECTION"
                            )

                            print(
                                f"Normal throttle: "
                                f"{NORMAL_THROTTLE}"
                            )

                            print(
                                f"Injected throttle: "
                                f"{ATTACK_THROTTLE}"
                            )

                            print(
                                "========================================"
                            )


                        else:

                            attack_type = "NONE"

                            print(
                                "\n"
                                "CYBER ATTACK DEACTIVATED"
                            )


                # --------------------------------------------
                # RESET STEERING
                # --------------------------------------------

                elif event.key == pygame.K_r:

                    control.steer = 0.0


        # ====================================================
        # MANUAL MODE
        # ====================================================

        if manual_mode:

            keys = pygame.key.get_pressed()


            # ------------------------------------------------
            # RESET
            # ------------------------------------------------

            requested_throttle = 0.0

            control.brake = 0.0


            # ------------------------------------------------
            # FORWARD
            # ------------------------------------------------

            if (
                keys[pygame.K_w]
                or
                keys[pygame.K_UP]
            ):

                requested_throttle = (
                    NORMAL_THROTTLE
                )

                control.reverse = False


            # ------------------------------------------------
            # REVERSE
            # ------------------------------------------------

            elif keys[pygame.K_x]:

                requested_throttle = (
                    REVERSE_THROTTLE
                )

                control.reverse = True


            # ------------------------------------------------
            # BRAKE
            # ------------------------------------------------

            elif (
                keys[pygame.K_s]
                or
                keys[pygame.K_DOWN]
            ):

                requested_throttle = 0.0

                control.brake = NORMAL_BRAKE


            # ------------------------------------------------
            # STEERING
            # ------------------------------------------------

            if (
                keys[pygame.K_a]
                or
                keys[pygame.K_LEFT]
            ):

                control.steer = -STEER_AMOUNT


            elif (
                keys[pygame.K_d]
                or
                keys[pygame.K_RIGHT]
            ):

                control.steer = STEER_AMOUNT


            else:

                control.steer *= 0.80


            # ------------------------------------------------
            # EMERGENCY BRAKE
            # ------------------------------------------------

            if keys[pygame.K_SPACE]:

                requested_throttle = 0.0

                control.brake = 1.0


            # ------------------------------------------------
            # CYBERSECURITY LAYER
            # ------------------------------------------------

            if (
                attack_active
                and
                requested_throttle > 0.0
                and
                control.brake == 0.0
            ):

                applied_throttle = ATTACK_THROTTLE


            else:

                applied_throttle = requested_throttle


            # ------------------------------------------------
            # APPLY CONTROL
            # ------------------------------------------------

            control.throttle = applied_throttle

            vehicle.apply_control(
                control
            )


        # ====================================================
        # AUTONOMOUS MODE
        # ====================================================

        else:

            # CARLA autopilot controls the vehicle

            requested_throttle = 0.0

            applied_throttle = 0.0

            control.brake = 0.0


        # ====================================================
        # TELEMETRY
        # ====================================================

        speed = get_speed()

        acceleration = get_acceleration()

        transform = vehicle.get_transform()

        location = transform.location


        csv_writer.writerow([

            time.time(),

            vehicle.id,

            round(location.x, 3),

            round(location.y, 3),

            round(location.z, 3),

            round(speed, 3),

            round(acceleration, 3),

            round(control.steer, 3),

            round(requested_throttle, 3),

            round(applied_throttle, 3),

            round(control.brake, 3),

            control.reverse,

            manual_mode,

            attack_active,

            attack_type

        ])


        csv_file.flush()


        # ====================================================
        # SMALL INFORMATION PANEL
        # ====================================================

        panel = pygame.Surface(
            (360, 175),
            pygame.SRCALPHA
        )

        # Semi-transparent black
        panel.fill(
            (0, 0, 0, 155)
        )


        screen.blit(
            panel,
            (15, 15)
        )


        # ====================================================
        # TITLE
        # ====================================================

        title = font_title.render(
            "CyberShield-DT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (30, 25)
        )


        # ====================================================
        # MODE
        # ====================================================

        if manual_mode:

            mode = "MANUAL"

        else:

            mode = "AUTONOMOUS"


        mode_text = font_main.render(

            f"Mode: {mode}",

            True,

            (255, 255, 255)

        )

        screen.blit(
            mode_text,
            (30, 58)
        )


        # ====================================================
        # SPEED
        # ====================================================

        speed_text = font_main.render(

            f"Speed: {speed:.1f} km/h",

            True,

            (255, 255, 255)

        )

        screen.blit(
            speed_text,
            (30, 82)
        )


        # ====================================================
        # CYBER STATUS
        # ====================================================

        if attack_active:

            cyber_status = "ATTACK"

        else:

            cyber_status = "NORMAL"


        cyber_text = font_main.render(

            f"Cyber: {cyber_status}",

            True,

            (255, 255, 255)

        )

        screen.blit(
            cyber_text,
            (30, 106)
        )


        # ====================================================
        # ATTACK
        # ====================================================

        attack_text = font_small.render(

            f"Attack: {attack_type}",

            True,

            (255, 255, 255)

        )

        screen.blit(
            attack_text,
            (30, 130)
        )


        # ====================================================
        # THROTTLE
        # ====================================================

        throttle_text = font_small.render(

            f"Throttle: "
            f"{requested_throttle:.2f} -> "
            f"{applied_throttle:.2f}",

            True,

            (255, 255, 255)

        )

        screen.blit(
            throttle_text,
            (30, 151)
        )


        # ====================================================
        # UPDATE DISPLAY
        # ====================================================

        pygame.display.flip()

        clock.tick(30)


# ============================================================
# ERROR HANDLING
# ============================================================

except KeyboardInterrupt:

    print(
        "\nController interrupted."
    )


except Exception as error:

    print(
        "\nController error:"
    )

    print(error)


# ============================================================
# CLEANUP
# ============================================================

finally:

    print(
        "\nStopping CyberShield-DT controller..."
    )


    try:

        vehicle.set_autopilot(False)

        control.throttle = 0.0
        control.brake = 1.0
        control.steer = 0.0
        control.reverse = False

        vehicle.apply_control(
            control
        )

        time.sleep(0.5)

    except Exception:

        pass


    try:

        camera.stop()

    except Exception:

        pass


    try:

        camera.destroy()

    except Exception:

        pass


    try:

        csv_file.close()

    except Exception:

        pass


    pygame.quit()


    print(
        "\nTelemetry saved to:"
    )

    print(
        TELEMETRY_FILE
    )

    print(
        "Controller stopped."
    )