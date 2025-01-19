#  see https://gpiozero.readthedocs.io/en/stable/api_input.html#rotaryencoder

from gpiozero import RotaryEncoder
from time import sleep

encoder = RotaryEncoder(17, 18)

while True:
    print("Value:", encoder.value)
    sleep(1)