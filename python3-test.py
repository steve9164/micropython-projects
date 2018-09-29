# File for testing parts of micropython intended code in a Python 3 environment

def wall_type(ball_next_x, ball_next_y):
  'Returns a tuple (isVerticalWall: Boolean, isHorizontalWall: Boolean)'

  # Preliminary write of wall collision checking
  # Technique:
  # - Store walls in lists of vertical and horizontal walls
  # - Do physics to calculate new position
  # - Check if there's a wall between old and new position
  #   + Walls for physics are thin (not 2 pixels as on display)
  #   + Loop over walls between horizontal positions
  #   + Calculate y position for each wall line
  #   + Check if that y position has a wall
  # - If there is, reverse velocity but use old positiom (impossible to go through walls, but bounces might be odd)
  

  # 3 rows of vertical walls, 3 columns of horizontal walls
  walls_v = [[False, False], [False, False], [False, True]]
  walls_h = [[True, False], [False, True], [True, False]]

  # Calculate which square the ball is and will be in
  square_x = ball_x//16
  square_y = ball_y//16
  square_next_x = ball_next_x//16
  square_next_y = ball_next_y//16

  if square_x == square_next_x and square_y == square_next_y:
    return (False, False)


  # Iteration direction
  start_x, stop_x = sorted([square_x, square_next_x])
  start_y, stop_y = sorted([square_y, square_next_y])
  # dir_y = 1 if square_next_y > square_y else -1
  is_v_wall = False
  for i in range(start_x, stop_x):
    # Intersection of line segment ball->ball_next and vertical wall i
    intersect_y = ball_y + (((i+1)*16-ball_x)*(ball_next_y-ball_y))//(ball_next_x-ball_x)
    # print('ball: ({},{}), next_ball: ({},{}), i: {}, intersect_y: {}'.format(ball_x, ball_y, ball_next_x, ball_next_y, i, intersect_y))
    if walls_v[intersect_y//16][i]:
      is_v_wall = True
      break

  is_h_wall = False
  for i in range(start_y, stop_y):
    # Intersection of line segment ball->ball_next and horizontal wall i
    intersect_x = ball_x + (((i+1)*16-ball_y)*(ball_next_x-ball_x))//(ball_next_y-ball_y)
    # print('ball: ({},{}), next_ball: ({},{}), i: {}, intersect_x: {}'.format(ball_x, ball_y, ball_next_x, ball_next_y, i, intersect_x))
    if walls_h[intersect_x//16][i]:
      is_h_wall = True
      break
      
  # is_v_wall = any(walls_v[square_y][i] for i in range(square_x, square_next_x, dir_x))
  # is_h_wall = any(walls_h[square_x][i] for i in range(square_y, square_next_y, dir_y))
  # This is buggy if there is diagonal movement
  # Instead when checking for vertical walls the correct y-level should be found using intersection of pos-change vector
  #  and each vertical wall. Should be able to do that math with integer division


  return (is_v_wall, is_h_wall)

def test_wall_type(ball: (int, int), ball_next: (int, int)):
  global ball_x
  global ball_y
  ball_x, ball_y = ball
  return wall_type(*ball_next)

import unittest

class TestWallCollisions(unittest.TestCase):
  def test_horizontal_wall(self):
    self.assertEqual(test_wall_type((3, 3), (9, 23)), (False, True))

  def test_diagonal_near_collision(self):
    self.assertEqual(test_wall_type((9, 8), (25, 24)), (False, False))

  def test_diagonal_collision(self):
    self.assertEqual(test_wall_type((7, 8), (23, 24)), (False, True))

  def test_other_diagonal_near_collision(self):
    self.assertEqual(test_wall_type((23, 24), (39, 8)), (False, False))

  def test_other_diagonal_collision(self):
    self.assertEqual(test_wall_type((25, 24), (41, 8)), (False, True))

  def test_long_no_collision(self):
    self.assertEqual(test_wall_type((40, 40), (24, 8)), (False, False))

  def test_vertical_wall(self):
    self.assertEqual(test_wall_type((21, 37), (36, 45)), (True, False))

  def test_diagonal_both(self):
    self.assertEqual(test_wall_type((23, 24), (39, 40)), (True, True))

  def test_diagonal_near_collision_both(self):
    self.assertEqual(test_wall_type((25, 24), (41, 40)), (False, False))


if __name__ == '__main__':
    unittest.main()
