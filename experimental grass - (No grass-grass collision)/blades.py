from collections import defaultdict
from settings import *
import random
import pygame as pg
import math

# --JOINT--
class Joint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# --BLADE--
class Blade:
    def __init__(self, root, color, length, thickness):
        # Grass thickness, grass length, grass color
        self.phase = random.uniform(0, math.tau)
        self.thickness = thickness
        self.length = length
        self.color = color

        # To check if blade is near player
        self.near_p = False
        self.root = root
        self.tip_x = root.x
        self.tip_y = root.y - length

        # Snap velocity
        self.vx = 0
        self.vy = 0

    def update(self):
        dx = self.root.x - self.tip_x
        #ax = dx * GRASS_STIFFNESS -> no swaying (setting origin at root x)
        wind = math.sin(pg.time.get_ticks() * 0.005 + self.phase) * 5
        ax = (dx + wind) * GRASS_STIFFNESS
        ay = GRASS_STIFFNESS

        # velocity update and move tip
        if not self.near_p:
            # spring back to its original x when player is not around
            self.vx += ax
            self.vx *= GRASS_DAMPING
            self.tip_x += self.vx

        # makes sure the tip always stay up
        self.vy -= ay
        self.vy *= GRASS_DAMPING
        self.tip_y += self.vy


        # ---- LENGTH CONSTRAINT (keeps blade length constant) ----
        # calculate vector from root to tip
        dx = self.tip_x - self.root.x
        dy = self.tip_y - self.root.y

        dist = math.hypot(dx, dy)

        if dist != 0:
            scale = self.length / dist
            # project tip onto circle of radius GRASS_LENGTH
            self.tip_x = self.root.x + dx * scale
            self.tip_y = self.root.y + dy * scale

    def draw(self, screen):
        pg.draw.polygon(screen,self.color,[(self.root.x - self.thickness, self.root.y),(self.root.x + self.thickness, self.root.y),(self.tip_x, self.tip_y)])
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
        self.place_cooldown = 50
        self.last_place_time = 0
        self.chunks = defaultdict(list) # {(chunk_x, chunk_y): [Blade, Blade, ...]} just so i dont forget
    
    def add_blade(self, x, y):
        chunk_x = x // CHUNK_SIZE
        chunk_y = y // CHUNK_SIZE

        if (len(self.chunks[(chunk_x, chunk_y)]) < 50):
            # CONTROLS GRASS LENGTH, GRASS COLOR, GRASS THICKNESS
            color = (random.randint(170, 200), random.randint(150, 170), 82) # randomizing color for depth
            length = random.randint(20, 30) # randomizes length so they look natural
            thickness = random.randint(3, 5) # randomizes thickness...so they look natural :D

            # snaps blade to bottom edge of current chunk
            self.chunks[(chunk_x, chunk_y)].append(Blade(Joint(x, y), color, length, thickness))
        return

    def remove_blades(self, x, y, radius=10):
        chunk_x = x // CHUNK_SIZE + 1
        chunk_y = y // CHUNK_SIZE + 1
        bottom_edge = (y//CHUNK_SIZE+1) * CHUNK_SIZE
        # Only check nearby chunks (same 3x3 logic)
        nearby_chunks = [
            (chunk_x+1, chunk_y),
            (chunk_x-1, chunk_y),
            (chunk_x, chunk_y)
        ]

        for chunk in nearby_chunks:
            blades = self.chunks[chunk]
            self.chunks[chunk] = [
                blade for blade in blades
                if (math.hypot(blade.root.x - x, blade.root.y - bottom_edge) > radius)
            ]

    def update(self):
        # determine which chunk the mouse is in
        player_x, player_y = pg.mouse.get_pos()
        player_cx = player_x // CHUNK_SIZE + 1
        player_cy = player_y // CHUNK_SIZE + 1

        # 3x3 grid around player (limits interaction checks)
        player_chunks = [
            (player_cx+1, player_cy),
            (player_cx-1, player_cy),
            (player_cx, player_cy)
        ]

        # spawn blade when mouse pressed
        mouse_pressed = pg.mouse.get_pressed()

        mouse_pressed = pg.mouse.get_pressed()
        current_time = pg.time.get_ticks()

        # LMB = Add blade
        if mouse_pressed[0]:
            if current_time - self.last_place_time >= self.place_cooldown:
                bottom_edge = (player_y // CHUNK_SIZE + 1) * CHUNK_SIZE
                self.add_blade(player_x, bottom_edge)
                self.last_place_time = current_time

        # RMB = Remove blade
        if mouse_pressed[2]:
            self.remove_blades(player_x, player_y, radius=10)

        # if not mouse_pressed[0]:
        #     self.holding_mouse = False

        # --- FIRST PASS: physics update --- O(n) for local blades
        for chunk in player_chunks:
            for blade in self.chunks[chunk]:
                distant_x = blade.tip_x - player_x
                distant_y = player_y - blade.tip_y
                normalized_distant = math.hypot(distant_x, distant_y)

                if 0 < normalized_distant < PUSH_RADIUS:
                    blade.near_p = True
                    if blade.tip_y > blade.root.y:
                        blade.tip_y = blade.root.y-2
                    nx = distant_x / normalized_distant
                    ny = distant_y / normalized_distant

                    strength = (PUSH_RADIUS - normalized_distant) / PUSH_RADIUS
                    push = strength * PUSH_FORCE

                    blade.tip_x += nx * push
                    blade.tip_y += ny * push
                else:
                    blade.near_p = False

                blade.update()


    # Chunk visualizer
    def draw_chunk_grid(self, screen, highlight_chunks=None):
        # Draw vertical lines
        for x in range(0, SCREEN_WIDTH, CHUNK_SIZE):
            pg.draw.line(screen, (60, 60, 80), (x, 0), (x, SCREEN_HEIGHT), 1)

        # Draw horizontal lines
        for y in range(0, SCREEN_HEIGHT, CHUNK_SIZE):
            pg.draw.line(screen, (60, 60, 80), (0, y), (SCREEN_WIDTH, y), 1)

        # Highlight specific chunks (like 3x3 active area)
        if highlight_chunks:
            for (cx, cy) in highlight_chunks:
                rect = pg.Rect(
                    cx * CHUNK_SIZE,
                    cy * CHUNK_SIZE,
                    CHUNK_SIZE,
                    CHUNK_SIZE
                )
                pg.draw.rect(screen, (120, 60, 60), rect, 2)

        # Debug texts
        font = pg.font.SysFont(None, 18)
        for x in range(0, SCREEN_WIDTH, CHUNK_SIZE):
            for y in range(0, SCREEN_HEIGHT, CHUNK_SIZE):
                cx = x // CHUNK_SIZE
                cy = y // CHUNK_SIZE
                text = font.render(f"{cx},{cy}", True, (150, 150, 150))
                screen.blit(text, (x + 4, y + 4))
                
# bitch....