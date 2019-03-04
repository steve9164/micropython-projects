import machine

spi = machine.SPI(1)
spi.init(baudrate=1000000)
rclk = machine.Pin(15, machine.Pin.OUT)
rclk.off()

ZERO  = 0b00111111
ONE   = 0b00000110
TWO   = 0b01011011
THREE = 0b01001111
FOUR  = 0b01100110
FIVE  = 0b01101101
SIX   = 0b01111101
SEVEN = 0b00000111
EIGHT = 0b01111111
NINE  = 0b01101111

digits = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

def display(digitBytes):
  rclk.off()
  spi.write(bytes(digitBytes))
  rclk.on()
