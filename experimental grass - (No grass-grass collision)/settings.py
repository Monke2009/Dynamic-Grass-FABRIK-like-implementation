import pygame as pg
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_COLOR = (25, 25, 40)
CHUNK_SIZE = 100 # 100 x 100

MIN_DIST = 1.5 # min distant between blades tips
PUSH_RADIUS = 30
PUSH_FORCE = 10

GRASS_DAMPING = 0.95
GRASS_STIFFNESS = 0.05

# HELPER FUNCTION
# --- DASHED LINES ---
def draw_dashed_line(surface, color, start_pos, end_pos, 
                     width=1, dash_length=2, gap_length=2):

    x1, y1 = start_pos
    x2, y2 = end_pos

    dx = x2 - x1 # distant x
    dy = y2 - y1 # distant y
    distance = math.hypot(dx, dy)

    if distance == 0:
        return

    dx /= distance
    dy /= distance

    dash_count = int(distance // (dash_length + gap_length))

    for i in range(dash_count):
        start_x = x1 + (dash_length + gap_length) * i * dx
        start_y = y1 + (dash_length + gap_length) * i * dy

        end_x = start_x + dash_length * dx
        end_y = start_y + dash_length * dy

        pg.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)