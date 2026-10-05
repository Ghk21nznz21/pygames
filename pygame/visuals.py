import pygame


def screen_update(screen, bk, bx, bx2, player, obstacles):
    """Draw the scrolling background, player and obstacles, then flip."""
    screen.blit(bk, (bx, 0))
    screen.blit(bk, (bx2, 0))
    player.draw(screen)
    for obs in obstacles:
        obs.draw(screen)
    pygame.display.update()
