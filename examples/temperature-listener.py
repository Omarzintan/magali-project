import sys
from subprocess import Popen, PIPE

# Store temperatures.
temperatures = []
sensor = Popen(['node', 'sensor.js'], stdout=PIPE)
buffer = b''
while True:

    # Read sensor data one char at a time
    out = sensor.stdout.read(1)

    # After a full reading...
    if out == b'\n':
        temperatures.append(float (buffer))
        print(temperatures)
        buffer = b''
    else:
        # Append to the buffer.
        buffer += out
