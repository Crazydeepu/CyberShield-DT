# ============================================================
# CyberShield-DT
# Main Project Launcher
# ============================================================

import subprocess
import sys
import time
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"

PYTHON = sys.executable

DIGITAL_TWIN = SRC / "digital_twin.py"
MANUAL_DRIVE = SRC / "manual_drive.py"
ANOMALY_DETECTOR = SRC / "anomaly_detector.py"


# ============================================================
# CHECK FILES
# ============================================================

print("===================================================")
print("CyberShield-DT")
print("===================================================")

print("\nChecking project files...")


required_files = [
    DIGITAL_TWIN,
    MANUAL_DRIVE,
    ANOMALY_DETECTOR
]


for file in required_files:

    if not file.exists():

        print("\nERROR: Required file not found:")
        print(file)

        input("\nPress ENTER to exit...")

        sys.exit(1)


print("All required files found.")


# ============================================================
# START DIGITAL TWIN
# ============================================================

print("\nStarting Digital Twin...")

digital_twin_process = subprocess.Popen(

    [
        PYTHON,
        str(DIGITAL_TWIN)
    ],

    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print("Digital Twin started.")


# ============================================================
# WAIT FOR DIGITAL TWIN
# ============================================================

print("\nWaiting for Digital Twin to initialize...")

time.sleep(8)


# ============================================================
# START ANOMALY DETECTOR
# ============================================================

print("\nStarting Anomaly Detector...")

anomaly_process = subprocess.Popen(

    [
        PYTHON,
        str(ANOMALY_DETECTOR)
    ],

    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print("Anomaly Detector started.")


# ============================================================
# WAIT FOR ANOMALY DETECTOR
# ============================================================

time.sleep(3)


# ============================================================
# START MANUAL CONTROLLER LAST
# ============================================================

print("\nStarting Manual / Autonomous Controller...")

manual_process = subprocess.Popen(

    [
        PYTHON,
        str(MANUAL_DRIVE)
    ],

    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print("Manual / Autonomous Controller started.")


# ============================================================
# PROJECT STATUS
# ============================================================

print("\n===================================================")
print("CYBERSHIELD-DT IS RUNNING")
print("===================================================")

print("\nActive components:")

print("  [1] Digital Twin")
print("  [2] Anomaly Detector")
print("  [3] Manual / Autonomous Controller")

print("\n===================================================")

print("IMPORTANT:")
print("Click the CyberShield-DT controller window once")
print("to make sure it has keyboard focus.")

print("\nManual Controls:")
print("  W / UP       -> Forward")
print("  S / DOWN     -> Brake")
print("  A / LEFT     -> Steer Left")
print("  D / RIGHT    -> Steer Right")
print("  X            -> Reverse")
print("  T            -> Manual / Autonomous")
print("  F            -> Throttle Injection")
print("  SPACE        -> Emergency Brake")
print("  R            -> Reset Steering")
print("  ESC          -> Exit")

print("===================================================")

print("\nPress ENTER here to stop the entire project.")


# ============================================================
# WAIT
# ============================================================

try:

    input()

except KeyboardInterrupt:

    pass


# ============================================================
# STOP PROJECT
# ============================================================

print("\nStopping CyberShield-DT...")


processes = [

    manual_process,
    anomaly_process,
    digital_twin_process

]


for process in processes:

    try:

        if process.poll() is None:

            process.terminate()

    except Exception:

        pass


time.sleep(2)


print("\nCyberShield-DT stopped.")

print("All processes terminated.")