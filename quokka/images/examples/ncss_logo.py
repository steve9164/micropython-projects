import quokka
from load_image import load_image

fb = load_image('NCSS-logo-68x50.qimz')

quokka.display.fill(1)
quokka.display.blit(fb, 30, 7)
quokka.display.show()

c = 1

while True:
  quokka.sleep(1500)
  quokka.display.invert(c)
  quokka.display.show()
  c = (c + 1) % 2
