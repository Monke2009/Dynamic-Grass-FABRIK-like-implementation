from collections import defaultdict
from settings import *
from random import randint
import pygame as pg
import math

# --JOINT--
class Joint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# --BLADE--
class Blade:
    def __init__(self, root, color):
        self.color = color
        self.near_p = False
        self.root = root
        self.tip_x = root.x
        self.tip_y = root.y - GRASS_LENGTH
        self.vx = 0
        self.vy = 0

    def update(self):
        dx = self.root.x - self.tip_x
        ax = dx * GRASS_STIFFNESS
        ay = GRASS_STIFFNESS

        # velocity update and move tip
        if not self.near_p:
            self.vx += ax
            self.vx *= GRASS_DAMPING
            self.tip_x += self.vx

            self.vy -= ay
            self.vy *= GRASS_DAMPING
            self.tip_y += self.vy


        # ---- LENGTH CONSTRAINT (keeps blade length constant) ----
        # calculate vector from root to tip
        dx = self.tip_x - self.root.x
        dy = self.tip_y - self.root.y

        dist = math.sqrt(dx * dx + dy * dy)

        if dist != 0:
            scale = GRASS_LENGTH / dist
            # project tip onto circle of radius GRASS_LENGTH (AKA make it POINT THE F*CK UP)
            self.tip_x = self.root.x + dx * scale
            self.tip_y = self.root.y + dy * scale

    def draw(self, screen):
        pg.draw.polygon(screen,self.color,[(self.root.x - 5, self.root.y),(self.root.x + 5, self.root.y),(self.tip_x, self.tip_y)])
        # pg.draw.line(
        #     screen,
        #     GRASS_COLOR,
        #     (self.root.x, self.root.y),
        #     (self.tip_x, self.tip_y),
        #     GRASS_WIDTH
        # )

# --CHUNKS--
class Chunks:
    def __init__ (self):
        self.holding_mouse = False
        self.chunks = defaultdict(list) # {(chunk_x, chunk_y): [Blade, Blade, ...]} just so i dont forget
    
    def add_blade(self, x, y):
        chunk_x = x // CHUNK_SIZE
        chunk_y = y // CHUNK_SIZE
        color = (randint(170, 200), randint(150, 170), 82)
        self.chunks[(chunk_x, chunk_y)].append(Blade(Joint(x, y), color))

    def update(self):
        # determine which chunk the mouse is in
        player_x, player_y = pg.mouse.get_pos()
        player_cx = player_x // CHUNK_SIZE
        player_cy = player_y // CHUNK_SIZE

        # 3x3 grid around player (limits interaction checks)
        player_chunks = [
            (player_cx+1, player_cy),
            (player_cx+1, player_cy-1),
            (player_cx+1, player_cy+1),
            (player_cx-1, player_cy),
            (player_cx-1, player_cy-1),
            (player_cx-1, player_cy+1),
            (player_cx, player_cy),
            (player_cx, player_cy-1),
            (player_cx, player_cy+1),
        ]

        # spawn blade when mouse pressed
        mouse_pressed = pg.mouse.get_pressed()
        if mouse_pressed[0] and self.holding_mouse == False:
            self.add_blade(player_x, player_y)
            self.holding_mouse = True
        if not mouse_pressed[0]: self.holding_mouse = False

        # --- FIRST PASS: physics update ---
        for chunk in player_chunks:
            for blade in self.chunks[chunk]:
                distant_x = blade.tip_x - player_x
                distant_y = blade.tip_y - player_y
                normalized_distant = math.sqrt(distant_x*distant_x + distant_y*distant_y)

                if 0 < normalized_distant < PUSH_RADIUS:
                    blade.near_p = True
                    if blade.tip_y > blade.root.y:
                        blade.tip_y = blade.root.y
                    nx = distant_x / normalized_distant
                    ny = distant_y / normalized_distant

                    strength = (PUSH_RADIUS - normalized_distant) / PUSH_RADIUS
                    push = strength * PUSH_FORCE

                    blade.tip_x += nx * push
                    blade.tip_y += ny * push
                else:
                    blade.near_p = False

                blade.update()

        for _ in range(2): # YEAH BABY MAKE IT SMOOTH HEEE HEEE~~ -MJ-....i made that up
            # --- SECOND PASS: Collision blocks for grass--- ...im tired boss
            for chunk in player_chunks:
                blades = self.chunks[chunk]
                for i in range(len(blades)):
                    for j in range(i + 1, len(blades)):
                        b1 = blades[i]
                        b2 = blades[j]

                        dx = b1.tip_x - b2.tip_x
                        dy = b1.tip_y - b2.tip_y
                        dist = math.sqrt(dx*dx + dy*dy)

                        MIN_DIST = 1.5

                        if 0 < dist < MIN_DIST:
                            nx = dx / dist
                            ny = dy / dist

                            overlap = (MIN_DIST - dist) * 0.5

                            b1.tip_x += nx * overlap
                            b1.tip_y += ny * overlap
                            b2.tip_x -= nx * overlap
                            b2.tip_y -= ny * overlap

                            b1.vx *= 0.8
                            b1.vy *= 0.8
                            b2.vx *= 0.8
                            b2.vy *= 0.8

            # --- THIRD PASS: re-apply length constraint ---
            for chunk in player_chunks:
                for blade in self.chunks[chunk]:
                    dx = blade.tip_x - blade.root.x
                    dy = blade.tip_y - blade.root.y
                    dist = math.sqrt(dx*dx + dy*dy)

                    if dist != 0:
                        scale = GRASS_LENGTH / dist
                        blade.tip_x = blade.root.x + dx * scale
                        blade.tip_y = blade.root.y + dy * scale
                
# bitch....