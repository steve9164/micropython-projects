from quokka import *
import radio

np = neopixel.NeoPixel()

radio.config(channel=15)
radio.on()

while True:
  msg_bytes = radio.receive_bytes()
  if msg_bytes:
#    msg_bytes = msg_bytes[2:]
    print(msg_bytes)
    for i in range(0, len(msg_bytes)-3, 3):
      pixel = [int(c) for c in msg_bytes[i:i+3]]
      np.set_pixel(i//3, pixel[0], pixel[1], pixel[2])
      np.show()
