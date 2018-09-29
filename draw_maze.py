# Maze for micropython (on quokka)
# Adapted from animation.py

from maze import MazeTree, Coordinate, get_neighbouring_coordinates
import quokka
import framebuf
import pyb

# Currently detects collision based on pixels
# Could instead track current square and only allow movement to adjacent square if there is no wall
# Also would be convenient for determing if you've won


ball_x = 6.0
ball_y = 6.0
#g = 10 # In pixels/s^2
v_x, v_y = 0.0,0.0
# For physics collisions and
# current_square = Coordinate(0, 0)

render_tick = False
physics_tick = False

# To get exception messages
import micropython
micropython.alloc_emergency_exception_buf(100)

###########################################################
### See new physics function wall_type in python3-test.py
###########################################################


# Cannot allocate memory inside callback
def render(t):
  global render_tick
  render_tick = True

def physics(t):
  global physics_tick
  physics_tick = True

render_timer = pyb.Timer(2, freq=60, callback=render)
physics_timer = pyb.Timer(3, freq=120, callback=physics)

def render_maze(m, fb):
  # Draw whole grid then remove walls that don't exist
  for x in range(8):
    fb.fill_rect(x*16, 0, 1, 64, 1)
    fb.fill_rect(x*16+15, 0, 1, 64, 1)

  for y in range(4):
    fb.fill_rect(0, y*16, 128, 1, 1)
    fb.fill_rect(0, y*16+15, 128, 1, 1)

  def remove_wall(coord1, coord2):
    'Remove wall between neighbouring squares at coord1 and coord2'
    coord = Coordinate(min(coord1.x, coord2.x), min(coord1.y, coord2.y))
    if coord1.x > coord.x or coord2.x > coord.x:
      fb.fill_rect(coord.x*16+15, coord.y*16+1, 2, 14, 0)
    elif coord1.y > coord.y or coord2.y > coord.y:
      fb.fill_rect(coord.x*16+1, coord.y*16+15, 14, 2, 0)
    else:
      print('Error: No wall removed for pair of coords ({0.x}, {0.y}) & ({1.x}, {1.y})'.format(coord1, coord2))

  def remove_walls(node):
    'Remove walls between node and its children'
    for child in node.children:
      remove_wall(node.coord, child.coord)
      remove_walls(child)

  remove_walls(m.tree)

# wall_dict = {}
# def generate_wall_dict(m):
#   def remove_wall(coord1, coord2):
#     wall_dict[{coord1, coord2}] = False
#   def remove_walls(node):
#     'Remove walls between node and its children'
#     for child in node.children:
#       remove_wall(node.coord, child.coord)
#       remove_walls(child)

#   # Generate walls between all squares in -1 to 4
#   for x in range(-1, 8):
#     for y in range(-1, 4):
#       wall_dict[{Coordinate(x, y), Coordinate(x+1, y)}] = True
#       wall_dict[{Coordinate(x, y), Coordinate(x, y+1)}] = True

#   remove_walls(m.tree)

# Make a maze and draw it to a framebuffer
my_maze = MazeTree(8, 4)
maze_framebuffer = framebuf.FrameBuffer(bytearray(quokka.display.pages*quokka.display.width), quokka.display.width, quokka.display.height, framebuf.MONO_VLSB)
render_maze(my_maze, maze_framebuffer)
# generate_wall_dict(my_maze)

def render_method():
  quokka.display.fill(0)
  quokka.display.blit(maze_framebuffer, 0, 0)
  quokka.display.text('S', my_maze.start_square.x*16+3, my_maze.start_square.y*16+3, 1)
  quokka.display.text('E', my_maze.end_square.x*16+3, my_maze.end_square.y*16+3, 1)
  # Draw ball
  x, y = round(ball_x), round(ball_y)
  quokka.display.fill_rect(x-1,y-1, 3, 3,1)

  quokka.display.show()

def physics_method():
  global t_old
  global v_x
  global v_y
  global ball_x
  global ball_y
  # global current_square

  # Make interval from last position and new position
  # Calculate the x-position on horizontals and y-position on verticals within that interval
  # Sort by closest
  # Check collisions
  # Then what?
  # What if I need another collision after the first?
  # Also, motion isn't linear

  # New idea:
  # Do simple integration
  # If vector of movement passes through a wall reverse velocity in x or y direction but don't update position
  # This may cause some odd positioning after bouncing off walls, but should mean that the ball will 
  #  never pass through a wall

  # Use simple Euler numerical integration

  t_new = pyb.millis()
  t_delta = (t_new - t_old)/1000.0
  t_old = t_new

  try:
    accel_vec = quokka.accelerometer.xyz
    a_y = -200.0*accel_vec[1]
    a_x = -200.0*accel_vec[0]
  except OSError as e:
    print('Accelerometer error: {}'.format(e))
    return

  # y
  v_y = v_y + a_y*t_delta
  ball_next_y = ball_y + v_y*t_delta

  # if ball_y < 0:
  #   ball_y = -ball_y
  #   v_y = -0.8*v_y
  # elif ball_y > 63:
  #   ball_y = 126 - ball_y
  #   v_y = -0.8*v_y

  # x
  v_x = v_x + a_x*t_delta
  ball_next_x = ball_x + v_x*t_delta

  if no_walls(ball_next_x, ball_next_y):
    ball_x = ball_next_x
    ball_y = ball_next_y


  # if ball_x < 0:
  #   ball_x = -ball_x
  #   v_x = -0.8*v_x
  # elif ball_x > 127:
  #   ball_x = 254 - ball_x
  #   v_x = -0.8*v_x

  if maze_framebuffer.pixel(int(ball_x), int(ball_y)) == 1:
    print('collision')
    if int(ball_x) % 16 == 0 and maze_framebuffer.pixel(int(ball_x), int(ball_y)-1) == 1:
      print('x left collision')
      v_x = -0.8*v_x
      ball_x += 1
    elif int(ball_x) % 16 == 15 and maze_framebuffer.pixel(int(ball_x), int(ball_y)+1) == 1:
      print('x right collision')
      v_x = -0.8*v_x
      ball_x -= 1
    if int(ball_y) % 16 == 0 and maze_framebuffer.pixel(int(ball_x)-1, int(ball_y)) == 1:
      print('y up collision')
      v_y = -0.8*v_y
      ball_y += 1
    elif int(ball_y) % 16 == 15 and maze_framebuffer.pixel(int(ball_x)+1, int(ball_y)) == 1:
      print('y down collision')
      v_y = -0.8*v_y
      ball_y -= 1

  # new_square = Coordinate(int(x/16.0), int(y/16.0))
  # if new_square != current_square:
  #   if new_square in get_neighbouring_coordinates(current_square):
  #     if not wall_dict[{current_square, new_square}]:
  #       # No wall
  #       current_square = new_square
  #     else:
  #       # Wall






t_old = pyb.millis()
while True:
  if render_tick:
    render_tick = False
    render_method()

  if physics_tick:
    physics_method()
    physics_tick = False



  quokka.sleep(1)




