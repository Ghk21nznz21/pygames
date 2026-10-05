"""No-Internet style jumper. Run: python jumper.py  (needs pygame)

Arrow keys move, space jumps. Assets load from ./utils relative to this file.
"""
import random
from pathlib import Path

import pygame
from pygame.locals import USEREVENT

from classes import Player, Obstacle
from visuals import screen_update

ASSETS = Path(__file__).parent / "utils"
WIDTH = HEIGHT = 500
PLAYER_SIZE = 50


def random_obs():
    return Obstacle(WIDTH - 1, 450, random.randint(10, 40), random.randint(50, 150))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("No Internet Jumper")

    img = pygame.transform.scale(
        pygame.image.load(str(ASSETS / "dot.png")), (PLAYER_SIZE, PLAYER_SIZE))
    bk = pygame.image.load(str(ASSETS / "simple_backround.jpg")).convert()

    bx, bx2 = 0, bk.get_width()
    clock = pygame.time.Clock()
    man = Player(250, 450, img)
    obstacles = []
    speed = 30

    pygame.time.set_timer(USEREVENT + 1, 500)                       # speed up
    pygame.time.set_timer(USEREVENT + 2, random.randint(4000, 5000))  # new obstacle

    run = True
    while run:
        screen_update(screen, bk, bx, bx2, man, obstacles)
        clock.tick(speed)

        for obs in list(obstacles):
            obs.x -= 1.4
            if obs.x < obs.width * -1:
                obstacles.remove(obs)

        bx -= 1.4
        bx2 -= 1.4
        if bx < bk.get_width() * -1:
            bx = bk.get_width()
        if bx2 < bk.get_width() * -1:
            bx2 = bk.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == USEREVENT + 1:
                speed += 1
            elif event.type == USEREVENT + 2:
                obstacles.append(random_obs())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
        if keys[pygame.K_RIGHT] and man.x < WIDTH - PLAYER_SIZE - man.vel:
            man.x += man.vel

        if not man.jump:
            if keys[pygame.K_SPACE]:
                man.jump = True
        else:
            if man.jumpcount >= -10:
                direc = 1 if man.jumpcount >= 0 else -1
                man.y -= (man.jumpcount ** 2) * 0.5 * direc  # parabola
                man.jumpcount -= 1
            else:
                man.jump = False
                man.jumpcount = 10

    pygame.quit()


if __name__ == "__main__":
    main()
