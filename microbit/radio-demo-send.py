import quokka
import radio
import sys

v = radio.version()
if not v:
  quokka.display.print('bad radio')
  quokka.display.show()
  sys.exit(0)

radio.on()
radio.config(channel=40)

while True:
  if quokka.buttons.a.is_pressed():
    quokka.neopixels.set_pixel(0, 64, 0, 0)
    radio.send("duck")
  elif quokka.buttons.b.is_pressed():
    radio.send("giraffe")
    quokka.neopixels.set_pixel(0, 0, 64, 0)
  else:
    radio.send("clear")
    quokka.neopixels.set_pixel(0, 0, 0, 64)
  sleep(10)
