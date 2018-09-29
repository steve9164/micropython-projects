# Maze for micropython (on quokka)
# By Stephen Davies

from maze import MazeTree, Coordinate, get_neighbouring_coordinates
import quokka
import framebuf
import pyb

ball_x = 6.0
ball_y = 6.0

v_x, v_y = 0.0,0.0
# For physics collisions and
# current_square = Coordinate(0, 0)

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

rt = pyb.Timer(2, freq=60, callback=render)
pt = pyb.Timer(3, freq=120, callback=physics)

def make_wall_map(m):
  'Produce a boolean map of vertical and horizontal walls'
  # walls is a tuple of (vertical_wall_map, horizontal_wall_map)
  # vertical_wall_map is a list of rows of walls, horizontal_wall_map is a list of columns of walls)
  walls_v = [[True]*(m.width-1) for _ in range(m.height)]
  walls_h = [[True]*(m.height-1) for _ in range(m.width)]
  def remove_wall(coord1, coord2):
    'Remove a wall between adjacent squares'
    coord = Coordinate(min(coord1.x, coord2.x), min(coord1.y, coord2.y))
    if coord1.x > coord.x or coord2.x > coord.x:
      walls_v[coord.y][coord.x] = False
    elif coord1.y > coord.y or coord2.y > coord.y:
      walls_h[coord.x][coord.y] = False
    else:
      print('Error: No wall removed for pair of coords ({0.x}, {0.y}) & ({1.x}, {1.y})'.format(coord1, coord2))
  
  def remove_walls(node):
    'Remove walls between node and its children'
    for child in node.children:
      remove_wall(node.coord, child.coord)
      remove_walls(child)

  remove_walls(m.tree)
  return (walls_v, walls_h)

def render_maze(walls, fb):
  'Render maze onto framebuffer'
  # Draw border
  fb.fill_rect(0, 0, 1, 64, 1)
  fb.fill_rect(127, 0, 1, 64, 1)
  fb.fill_rect(1, 0, 126, 1, 1)
  fb.fill_rect(1, 63, 126, 1, 1)

  # Draw inner walls
  for y, row in enumerate(walls[0]):
    for x, is_wall in enumerate(row, 0):
      if is_wall:
        fb.fill_rect(x*16+15, y*16, 2, 16, 1)
  for x, col in enumerate(walls[1]):
    for y, is_wall in enumerate(col, 0):
      if is_wall:
        fb.fill_rect(x*16, y*16+15, 16, 2, 1)  


# Make a maze and draw it to a framebuffer
my_maze = MazeTree(8, 4)
wall_map = make_wall_map(my_maze)
maze_framebuffer = framebuf.FrameBuffer(bytearray(quokka.display.pages*quokka.display.width), quokka.display.width, quokka.display.height, framebuf.MONO_VLSB)
render_maze(wall_map, maze_framebuffer)

def render_method():
  quokka.display.fill(0)
  quokka.display.blit(maze_framebuffer, 0, 0)
  quokka.display.text('S', my_maze.start_square.x*16+3, my_maze.start_square.y*16+3, 1)
  quokka.display.text('E', my_maze.end_square.x*16+3, my_maze.end_square.y*16+3, 1)
  
  # Draw ball
  x, y = int(ball_x), int(ball_y)
  quokka.display.fill_rect(x-1,y-1, 3, 3,1)

  quokka.display.show()

def wall_type(walls, ball_nx_x, ball_nx_y):
  'Returns a tuple (isVerticalWall: Boolean, isHorizontalWall: Boolean)'
  walls_v, walls_h = walls

  # Calculate which square the ball is and will be in
  sq_x = int(ball_x//16)
  sq_y = int(ball_y//16)
  sq_nx_x = int(ball_nx_x//16)
  sq_nx_y = int(ball_nx_y//16)

  if sq_x == sq_nx_x and sq_y == sq_nx_y:
    return (False, False)

  # Iteration direction
  start_x, stop_x = sorted([sq_x, sq_nx_x])
  start_y, stop_y = sorted([sq_y, sq_nx_y])
  # dir_y = 1 if square_nx_y > square_y else -1
  is_v_wall = False
  for i in range(start_x, stop_x):
    # Intersection of line segment ball->ball_nx and vertical wall i
    intersect_y = int(ball_y + (((i+1)*16-ball_x)*(ball_nx_y-ball_y))/(ball_nx_x-ball_x))
    if walls_v[intersect_y//16][i]:
      is_v_wall = True
      break

  is_h_wall = False
  for i in range(start_y, stop_y):
    # Intersection of line segment ball->ball_nx and horizontal wall i
    intersect_x = int(ball_x + (((i+1)*16-ball_y)*(ball_nx_x-ball_x))/(ball_nx_y-ball_y))
    if walls_h[intersect_x//16][i]:
      is_h_wall = True
      break

  return (is_v_wall, is_h_wall)

def physics_method():
  global t_old
  global v_x
  global v_y
  global ball_x
  global ball_y

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
  ball_nx_y = ball_y + v_y*t_delta

  # x
  v_x = v_x + a_x*t_delta
  ball_nx_x = ball_x + v_x*t_delta

  # Check crossing outer border. 
  # Must be done before collision detection because the algorithm crashes for out of bounds coordinates
  skip_collision = False
  if ball_nx_x < 0 or ball_nx_x > 128:
    v_x = -0.8*v_x
    skip_collision = True
  if ball_nx_y < 0 or ball_nx_y > 64:
    v_y = -0.8*v_y
    skip_collision = True
  if skip_collision:
    return
  
  # Determine the types of walls that the ball will pass through to get to ball_nx and deflect off them
  v_wall, h_wall = wall_type(wall_map, ball_nx_x, ball_nx_y)
  if v_wall:
    v_x = -0.8*v_x
  if h_wall:
    v_y = -0.8*v_y
  if not(v_wall) and not(h_wall):
    # No collision. Advance ball
    ball_x = ball_nx_x
    ball_y = ball_nx_y


t_old = pyb.millis()
while True:
  if render_tick:
    render_tick = False
    render_method()

  if physics_tick:
    physics_method()
    physics_tick = False

  quokka.sleep(1)




