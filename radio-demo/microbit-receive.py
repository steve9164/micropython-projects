from microbit import *

import radio

radio.config(channel=40)

radio.on()

while True:
  msg = radio.receive()
  if msg is not None:
    if msg == "duck":
      display.show(Image.DUCK)
    elif msg == "giraffe":
      display.show(Image.GIRAFFE)
    elif msg == "clear":
      display.clear()

