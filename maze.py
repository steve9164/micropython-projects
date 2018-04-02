# From https://github.com/steve9164/maze-generator

'''
Maze Generator
By Stephen Davies

Builds a maze using tree construction
'''

# Current idea:
# - Build maze and tree at the same time
# - Start at some square - say (0, 0) for now - and randomly add unused square to leaves of the tree

import random
from collections import namedtuple
SquareNode = namedtuple('SquareNode', ['coord', 'children'])
Coordinate = namedtuple('Coordinate', ['x', 'y'])

def get_neighbouring_coordinates(coord, width, height):
    'Get neighbouring coordinates that also lie in the rectangle'
    return (
        ([Coordinate(coord.x-1, coord.y)] if coord.x > 0 else []) +
        ([Coordinate(coord.x+1, coord.y)] if coord.x < width-1 else []) +
        ([Coordinate(coord.x, coord.y-1)] if coord.y > 0 else []) +
        ([Coordinate(coord.x, coord.y+1)] if coord.y < height-1 else [])
    )


class MazeTree(object):
    'A maze represented as a tree of squares (each with coordinates of their position in the maze)'
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.start_square = Coordinate(0,0)
        self.tree = SquareNode(coord=self.start_square, children=[])
        tree_nodes = [self.tree]
        used_squares = set([self.tree.coord])
        while len(used_squares) < width*height:
            # Choose a square to add to the maze, and the node it should be added to
            all_choices = [(adjacent, node) for node in tree_nodes for adjacent in set(get_neighbouring_coordinates(node.coord, width, height)) - used_squares]
            next_square, node = random.choice(all_choices)
            # Create the new node and place it in the MazeTree
            new_node = SquareNode(coord=next_square, children=[])
            node.children.append(new_node)
            # Record the new node and the square it occupies
            tree_nodes.append(new_node)
            used_squares.add(next_square)
        # Now that the maze is built, choose the longest (break ties randomly) and use
        #  the leaf as the end square of the maze
        paths = self.list_paths()
        max_path_length = max(len(path) for path in paths)
        maze_path = random.choice([path for path in paths if len(path) == max_path_length])
        self.end_square = maze_path[-1].coord


    def list_paths(self):
        'Find all paths from the root node to leaf nodes'
        def generate_directed_paths(node):
            'Generate a list of directed paths from the given node to each leaf'
            if node.children:
                return [[node] + path for child in node.children for path in generate_directed_paths(child)]
            else:
                return [[node]]
        return generate_directed_paths(self.tree)
