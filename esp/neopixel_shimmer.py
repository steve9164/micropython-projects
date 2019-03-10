
import time


def shimmer(mode0, mode1, period_t, total_t, np):
    cycle_start_t = time.ticks_ms()
    start_t = cycle_start_t
    while time.ticks_diff(time.ticks_ms(), start_t) < total_t:
        cycle_progress = 2*time.ticks_diff(time.ticks_ms(), cycle_start_t)/period_t
        if cycle_progress >= 2.0:
            cycle_start_t = time.ticks_ms()
            continue
        mult = abs(1-cycle_progress)
        for i in range(144):
            col = tuple(int(b0*mult + b1*(1-mult)) for (b0, b1) in zip(mode0[i], mode1[i]))
            np[i] = col
        np.write()

def run():
    import machine, neopixel
    np = neopixel.NeoPixel(machine.Pin(0), 144)
    m0 = [(((i+1)%2)*48,0,0) for i in range(144)]
    m1 = [(0,(i%2)*48,0) for i in range(144)]
    shimmer(m0, m1, 4000, 30000, np)

