import pygame
import sys


from Network import Network
from client_visuals import *

pygame.font.init()
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")



def main():
    global N
    run = True
    clock = pygame.time.Clock()
    playerID = int(N.get_playerID())  # returns PLAYER ID in that GAME
    print("You are player", playerID)
    exitt = False
    while run:
        clock.tick(60)
        try:
            game = N.exchange_objs("GET GAME")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.both_DONE():
            redraw_MAIN_Window(screen, game, playerID)
            pygame.time.delay(500)
            try:
                game = N.exchange_objs("RESTART")
            except:
                run = False
                break

            font = pygame.font.SysFont("comicsans", 90)
            #PLAYER1 = 0 ; PLAYER2= 1 ; TIE = -1
            # PLAYER1-ID= 0; PLAYER2-ID= 1;
            winner = game.winner()
            if (winner == 0 and playerID == 0) or (winner == 1 and playerID == 1):
                text = font.render("You Won!", 1, (255, 0, 0))
            elif winner == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            screen.blit(text, (width/2 - text.get_width() /
                        2, height/2 - text.get_height()/2))

            # WINNER WINDOW
            pygame.display.update()
            pygame.time.delay(2000)

            # BREAK TO MENU
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exitt = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    # only able to chose when both connected
                    if btn.button_clicked(pos) and game.connected():
                        if playerID == 0:
                            # CHECK IF ALREADY CHOOSE ->DONT ALLOW CHANGES ON MOVES
                            if not game.p1STATUS:
                                N.exchange_objs(btn.text)
                        else:
                            if not game.p2STATUS:  # DONT ALLOW CHANGES ON MOVES
                                N.exchange_objs(btn.text)

        # extend exit to to some unkown pygame exit error
        if exitt:
            pygame.quit()
        else:
            redraw_MAIN_Window(screen, game, playerID)


def Get_Stats():
    global N
    run = True
    stats = N.receive_stats()
    while run:
        screen.fill((128, 128, 128))
        #STATS = { "Time_Played" :stats[0],"Wins": stats[1], "Loses": stats[2], "Ties": stats[3]}
        STATS = {"Wins": stats[0], "Loses": stats[1], "Ties": stats[2]}
        distance = 0
        font = pygame.font.SysFont("Times New Roman", 30)
        for key, value in STATS.items():
            key_text = font.render(key, 1, (255, 0, 0))
            value_text = font.render(str(value), 1, (255, 0, 0))
            screen.blit(key_text, (600/2 - key_text.get_width()/2,
                        (100+distance)/2 - key_text.get_height()/2))
            screen.blit(value_text, (750/2 - value_text.get_width()/2,
                        (100+distance)/2 - value_text.get_height()/2))
            distance += 100

        return_to_menu = Button("Return to Menu", 250,
                                500, 300, 200, (0, 0, 0))
        return_to_menu.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if return_to_menu.button_clicked(pos):
                    run = False


def menu_screen():
    '''
    Start client connection 
    Create buttons 
    listen to player movements 
    Exchange update game for player movements
    '''
    
    global N
    N = Network()  # create 1 per client instead of per game
    N.connect()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        screen.fill((128, 128, 128))
        start_btn = Button("Start Game", 100, 350, 250, 200, (0, 0, 0))
        show_stats = Button("Get Stats", 400, 350, 250, 200, (0, 0, 0))
        start_btn.draw(screen)
        show_stats.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                N.exchange_instructions('Close Connection')
                pygame.quit()
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.button_clicked(pos):
                    N.exchange_instructions('Start Game')
                    main()
                elif show_stats.button_clicked(pos):
                    N.exchange_instructions("Get Stats")
                    Get_Stats()


try:
    menu_screen()
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit()