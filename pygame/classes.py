import pygame


class Obstacle:
    """A scrolling obstacle block."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect)  # brown


class Player:
    """The jumping player."""

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.vel = 4
        self.jump = False
        self.jumpcount = 10

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
