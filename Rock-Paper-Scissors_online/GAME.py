from pygame.locals import *

class Game:
    ''' 
    Starts a game and tracks the status of the game.
    Needs a running server and 2 players connected to the server.
    '''
    def __init__(self, id):  
        """Initialize the Game class."""
        self.p1STATUS = False  # Tracks if player 1 has made a choice
        self.p2STATUS = False  # Tracks if player 2 has made a choice
        self.ready = False  # Tracks if both players are connected
        self.id = id  # Game id
        self.choises = [0, 0]  # Stores the choices of the players
        self.wins = [0, 0]  # Stores the wins of the players
        self.ties = 0  # Stores the number of ties

        self.p1_left = False  # Tracks if player 1 has left the game
        self.p2_left = False  # Tracks if player 2 has left the game

    def connected(self):
        """Check if both players are connected."""
        return self.ready

    def get_player_choise(self, playerID):
        """Return the choice of the specified player."""
        return self.choises[playerID]

    def UPDATE_CHOISE(self, playerID, choise):
        """Update the choice of the specified player."""
        self.choises[playerID] = choise
        if playerID == 0:
            self.p1STATUS = True
        else:
            self.p2STATUS = True

    def both_DONE(self):
        """Check if both players have made a choice."""
        return self.p1STATUS and self.p2STATUS

    def winner(self):
        """
        Determine the winner of the game based on the choices of the players.
        The choices are compared based on the rules of Rock, Paper, Scissors.
        """
        p1 = self.choises[0].upper()[0]
        p2 = self.choises[1].upper()[0]

        winner = -1  # Default value indicating a tie
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        if winner == -1:
            self.ties += 0.5
        else:
            self.wins[winner] += 0.5

        return winner

    def leave(self, playerID):
        """Update the status of the specified player to indicate they have left the game."""
        if playerID == 0:
            self.p1_left = True
        else:
            self.p2_left = True

    def end_game(self):
        """Check if both players have left the game."""
        return self.p1_left and self.p2_left