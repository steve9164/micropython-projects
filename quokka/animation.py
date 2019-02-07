import quokka
import pyb

quokka.display.fill(0)
quokka.display.show()


ball_x = 40.0
ball_y = 6.0
#g = 10 # In pixels/s^2
v_x, v_y = 0.0,0.0

render_tick = False
physics_tick = False

# To get exception messages
import micropython
micropython.alloc_emergency_exception_buf(100)

# Cannot allocate memory inside callback
def render(t):
  global render_tick
  render_tick = True

def physics(t):
  global physics_tick
  physics_tick = True

render_timer = pyb.Timer(2, freq=60, callback=render)
physics_timer = pyb.Timer(3, freq=120, callback=physics)



t_old = pyb.millis()
while True:
  if render_tick:
    print('rendering')
    render_tick = False
    quokka.display.fill(0)
    x, y = round(ball_x), round(ball_y)
    quokka.display.fill_rect(x-1,y-1, 3, 3,1)
    quokka.display.show()

  if physics_tick:
    print('physics tick')
    physics_tick = False

    t_new = pyb.millis()
    t_delta = (t_new - t_old)/1000.0
    t_old = t_new

    # y
    a_y = -200.0*quokka.accelerometer.y
    v_y = v_y + a_y*t_delta
    ball_y = ball_y + v_y*t_delta
    
    if ball_y < 0:
      ball_y = -ball_y
      v_y = -0.8*v_y
    elif ball_y > 63:
      ball_y = 126 - ball_y
      v_y = -0.8*v_y

    
    # x
    a_x = -200.0*quokka.accelerometer.x
    v_x = v_x + a_x*t_delta
    ball_x = ball_x + v_x*t_delta
    if ball_x < 0:
      ball_x = -ball_x
      v_x = -0.8*v_x
    elif ball_x > 127:
      ball_x = 254 - ball_x
      v_x = -0.8*v_x

  quokka.sleep(10)
