import pygame
from os import path

maze_filename = 'maze.bmp'

def transform_maze():
    src = pygame.image.load(path.join(path.dirname(__file__),maze_filename))
    dst = pygame.Surface((61,61))

    src.lock()
    dst.lock()
    for x in range(5, 615, 10):
        for y in range(5, 615, 10):
            c = src.get_at((x,y))
            dst.set_at((int((x - 5)/10), int((y-5)/10)), c)

    src.unlock()
    dst.unlock()

    pygame.image.save(dst, path.join(path.dirname(__file__),maze_filename))

def read_maze_img():
    maze_img = pygame.image.load(path.join(path.dirname(__file__),maze_filename))
    maze = []
    maze_size = maze_img.get_size()

    maze_img.lock()
    for y in range(maze_size[1]):
        row = []
        for x in range(maze_size[0]):
            color = maze_img.get_at((x,y))
            if color == (255, 255, 255, 255):   #walkable
                row.append(0)
            else:
                row.append(1)       #wall
        maze.append(row)
    maze_img.unlock()

    return maze

def build_maze_image(maze_matrix, zoom):
    rows, cols = get_maze_size(maze_matrix)
    maze_img = pygame.Surface((cols* zoom, rows * zoom))
    maze_img.lock()
    for row in range(rows):
        for col in range(cols):
            color = (255, 255, 255, 255) if maze_matrix[row][col] == 0 else (0, 0, 0, 255)
            for x in range(zoom):
                for y in range(zoom):
                    maze_img.set_at(((col* zoom) + x,(row * zoom) + y), color)
    maze_img.unlock()

    return maze_img

def get_maze_size(maze_matrix):
    return len(maze_matrix), len(maze_matrix[0])

def screen_point_to_maze_coord(zoom, point):  # returns row, col
    return int(point[1] / zoom), int(point[0] / zoom)

def maze_coord_to_screen_point(zoom, coord):  # returns x,y
    return coord[1] * zoom, coord[0] * zoom

def maze_coord_is_walkable(maze_matrix, coord):
    return maze_matrix[int(coord[0])][int(coord[1])] == 0