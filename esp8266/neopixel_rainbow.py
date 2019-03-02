
import time, math
import machine, neopixel


colors = [
    (158,1,66),
    (213,62,79),
    (244,109,67),
    (253,174,97),
    (254,224,139),
    (255,255,191),
    (230,245,152),
    (171,221,164),
    (102,194,165),
    (50,136,189),
    (94,79,162)
]

def interpolate(l, fractional_index):
    frac, index = math.modf(fractional_index)
    i = int(index)
    if i >= len(l)-1:
        return l[-1]
    else:
        return tuple(round((1-frac)*c0 + frac*c1) for c0, c1 in zip(l[i], l[i+1]))


def generate_rainbow(n):
    interp_list = [interpolate(colors, i/(n-1)*(len(colors)-1)) for i in range(n)]
    return [(r//16, g//16, b//16) for (r,g,b) in interp_list] 

def show_rainbow():
    np = neopixel.NeoPixel(machine.Pin(0), 144)
    for i, c in enumerate(generate_rainbow(144)):
        np[i] = c
    np.write()

def shifting_rainbow():
    np = neopixel.NeoPixel(machine.Pin(0), 144)
    rainbow = generate_rainbow(72)
    rainbow.extend(rainbow[::-1])
    for _ in range(10):
        for _ in range(144):
            rainbow = [rainbow[-1]] + rainbow[:-1]
            for i, c in enumerate(rainbow):
                np[i] = c
            np.write()

