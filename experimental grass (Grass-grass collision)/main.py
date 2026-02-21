import pygame as pg
import math
from settings import *
import random
from blades import Chunks

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Grass Test")
font = pg.font.SysFont(None, 18)
clock = pg.time.Clock()
chunks = Chunks()

# PRESET GRASS PATCH
# for i in range(0, 100):
#     chunks.add_blade((SCREEN_WIDTH/2)-250+i*5, SCREEN_HEIGHT/2)
text = "-[LMB] to place [RMB] to remove grass blade-"

running = True

# while loop----------------------------------------------------------
while running:
    clock.tick(120)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- UPDATE ---
    chunks.update() # Disgusting hack used to update every blades even when player isnt in chunk
    for chunk in chunks.chunks.values():
        for blade in chunk:
            blade.update()

    # --- DRAW ---
    screen.fill((30, 30, 40))

    # Get mouse position snaps into bottom edge & updating player adjacent chunks
    mouse_pressed = pg.mouse.get_pressed()
    player_x, player_y = pg.mouse.get_pos()
    player_cx = player_x // CHUNK_SIZE
    player_cy = player_y // CHUNK_SIZE
    bottom_edge = (player_y//CHUNK_SIZE+1) * CHUNK_SIZE
    color1 = (220, 75, 75) if mouse_pressed[2] else (255, 255, 255)
    color2 = (103, 40, 40) if mouse_pressed[2] else (156, 156, 156)
    
    # 3x3 grid around player (limits interaction checks)
    player_chunks = [
            (player_cx+1, player_cy),
            (player_cx-1, player_cy),
            (player_cx, player_cy)
        ]

    pg.draw.circle(screen, (color1), (player_x, player_y), PUSH_RADIUS/4)
    draw_dashed_line(screen, (color2), (player_x, player_y), (player_x, bottom_edge), 2)
    for chunk in chunks.chunks.values():
        for blade in chunk:
            blade.draw(screen)
        
    chunks.draw_chunk_grid(screen, player_chunks)
    pg.draw.line(screen, (color1), (player_x - 5, bottom_edge), (player_x + 5, bottom_edge), 4)

    # ---Render text---
    text_surface = font.render(text, True, (200, 200, 200))
    text_rect = text_surface.get_rect()
    text_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
    screen.blit(text_surface, text_rect)

    pg.display.flip()

pg.quit()