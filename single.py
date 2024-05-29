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

# Durations in nanoseconds
total_duration = 0
max_duration = 0
min_duration = float('inf')
# Initialize reference time measurement
t1 = datetime.datetime.now()

# We need iterator value after the loop
i = 0

print("Reading", end="", flush=True)

# Take the measurements!
while not exit_flag and i < 100000:
    try:
        # Read the range. Note that it's a blocking call
        distance = tof.get_distance()
    except Exception as error:
        print(f"\rError getting measurement: {error}")
        distance = 8096

    # Check IO timeout and print range information
    if distance == 0:
        print(f"\rReading{i} | timeout!", end="", flush=True)
    else:
        print(f"\rReading{i} | {distance}mm", end="", flush=True)

    # Calculate duration of current iteration
    t2 = datetime.datetime.now()
    duration = (t2 - t1).total_seconds() * 1e9  # Convert to nanoseconds
    # Save current time as reference for next iteration
    t1 = t2
    # Add total measurements duration
    total_duration += duration
    # Skip comparing first measurement against max and min as it's not a full iteration
    if i == 0:
        continue
    # Check and save max and min iteration duration
    if duration > max_duration:
        max_duration = duration
    if duration < min_duration:
        min_duration = duration
    
    i += 1

# Print duration data
print(f"\nMax duration: {max_duration}ns")
print(f"Min duration: {min_duration}ns")
print(f"Avg duration: {total_duration/(i+1)}ns")
print(f"Avg frequency: {1e9/(total_duration/(i+1))}Hz")

# Stop ranging
tof.stop_ranging()
