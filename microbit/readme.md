# SSD1306 on micro:bit

Flash to micro:bit using the following:

```
uflash -r firmware-with-framebuffer.hex ssd1306.py
```

Then use `oled` in the REPL like so:

```
oled.framebuffer.text('micro:bit OLED', 4, 4)
oled.show()
```

