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
  if quokka.button_a.is_pressed():
    quokka.display.print('send a')
    #quokka.neopixels.set_pixel(0, 64, 0, 0)
    radio.send("duck")
  elif quokka.button_b.is_pressed():
    radio.send("giraffe")
    #quokka.neopixels.set_pixel(0, 0, 64, 0)
  else:
    radio.send("clear")
    #quokka.neopixels.set_pixel(0, 0, 0, 64)
  quokka.sleep(10)
