from quokka import *
import radio
import ubinascii

np = neopixel.NeoPixel()

radio.config(channel=15)
radio.on()

while True:
  msg = radio.receive()
  if msg:
    print(msg)
    msg_bytes = ubinascii.a2b_base64(msg)
    print(msg_bytes)
    for i in range(0, len(msg_bytes)-3, 3):
      pixel = [int(c) for c in msg_bytes[i:i+3]]
      np.set_pixel(i//3, pixel[0], pixel[1], pixel[2])
      np.show()
