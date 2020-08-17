import random, time
while True:
    # Wait 0 to 5 seconds
    time.sleep(random.random() * 5)
    # Set any temperature from -5 to 15
    temperature = (random.random() * 20) -5
    # We flush in order to ensure that the information arrives when we expect it to.
    print(temperature, flush=True, end='')
