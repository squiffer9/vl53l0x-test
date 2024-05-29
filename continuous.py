import signal
import sys
import time
import VL53L0X
import datetime

# SIGINT (CTRL-C) exit flag and signal handler
exit_flag = False

def sigint_handler(signum, frame):
    global exit_flag
    exit_flag = True

signal.signal(signal.SIGINT, sigint_handler)

# Create the sensor with default values
tof = VL53L0X.VL53L0X()

try:
    # Open the I2C connection to the sensor
    tof.open()

    # Set accuracy mode
    tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
except Exception as error:
    print(f"Error initializing sensor: {error}")
    sys.exit(1)

print("Reading measurements. Press Ctrl+C to stop.")

# Continuously take measurements and output the results
while not exit_flag:
    try:
        # Read the range. Note that it's a blocking call
        distance = tof.get_distance()
    except Exception as error:
        print(f"\rError getting measurement: {error}")
        distance = 8096

    # Check IO timeout and print range information
    if distance == 0:
        print("Timeout!", flush=True)
    else:
        print(f"Distance: {distance} mm", flush=True)

    # Sleep for a short interval to avoid flooding the output
    time.sleep(0.1)

# Stop ranging
tof.stop_ranging()

print("Measurement stopped.")
