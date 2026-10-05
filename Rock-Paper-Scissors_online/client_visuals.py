import pygame

class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Times New Roman", 30)
        text = font.render(self.text, 1, (255, 255, 255))
        screen.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                    self.y + round(self.height/2) - round(text.get_height()/2)))

    def button_clicked(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_MAIN_Window(screen, game, playerID):
    try:
        screen.fill((128, 128, 128))
    except:
        print('erro')

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        screen.blit(text, (screen.get_width()/2 - text.get_width() /
                    2, screen.get_height()/2 - text.get_height()/2))
    else:
        # CONSTANT TEXT DISPLAY
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        screen.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        screen.blit(text, (380, 200))

        # CHANGING TEXT BASED ON GAME STATUS AND PLAYER
        move1 = game.get_player_choise(0)
        move2 = game.get_player_choise(1)
        # both played show moves
        if game.both_DONE():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            # player1 played and player1 screen/connection
            if game.p1STATUS and playerID == 0:
                text1 = font.render(move1, 1, (0, 0, 0))

            # player1 played and player2 screen/connection
            elif game.p1STATUS:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            # player1 didnt played yet and player2 screen/connection
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            # player2 played and player2 screen/connection
            if game.p2STATUS and playerID == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            # ...
            elif game.p2STATUS:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        # which player screen/connection we are
        if playerID == 1:
            screen.blit(text2, (100, 350))
            screen.blit(text1, (400, 350))
        else:
            screen.blit(text1, (100, 350))
            screen.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(screen)

    pygame.display.update()


btns = [
    Button("Rock", 50, 500, 100, 150, (0, 0, 0)), 
    Button("Scissors", 250, 500, 100, 150, (255, 0, 0)), 
    Button("Paper", 450, 500, 100, 150, (0, 255, 0))
]

