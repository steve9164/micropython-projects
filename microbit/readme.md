# SSD1306 on micro:bit

Flash to micro:bit using the following:

```
uflash -r firmware-with-framebuffer.hex ssd1306.py
```

Then use `oled` in the REPL like so:

```py
oled.framebuffer.text('micro:bit OLED', 4, 4)
oled.framebuffer.blit(ncss, 30, 16)
oled.show()
```

## Bulding custom firmware with framebuffer

Modified firmware at https://github.com/steve9164/bbcmicrobit-micropython/tree/with_framebuf

Clone with:
```
git clone https://github.com/steve9164/bbcmicrobit-micropython.git --branch with_framebuf
```
and build according to microbit firmware build instructions.