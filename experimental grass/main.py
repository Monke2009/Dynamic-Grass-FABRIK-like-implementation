import pygame as pg
from settings import *
from blades import Chunks

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Grass Test")
clock = pg.time.Clock()

chunks = Chunks()
for i in range(0, 100):
    chunks.add_blade((SCREEN_WIDTH/2)-250+i*5, SCREEN_HEIGHT/2)

running = True
while running:
    clock.tick(120)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- UPDATE ---
    chunks.update()

    # Chunk update
    for chunk in chunks.chunks.values():
        for blade in chunk:
            blade.update()

    # --- DRAW ---
    screen.fill((30, 30, 40))

    for chunk in chunks.chunks.values():
        for blade in chunk:
            blade.draw(screen)

    pg.display.flip()

pg.quit()