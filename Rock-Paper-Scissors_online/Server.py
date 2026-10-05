import os
import socket
import sys
from _thread import *
from GAME import Game
import pickle

# Global variables for port number and server IP
global port_n
global server
port_n = 5555
server = os.getenv('RPS_SERVER', '127.0.0.1')


def create_socket():
    """Create a new socket for the server."""
    global session
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def bind_socket():
    """Bind the server socket to the specified IP and port."""
    try:
        session.bind((server, port_n))
        print('binding done:', session.getsockname())
    except socket.error as e:
        print(str(e))
    session.listen(2)
    print('Server started')


def accept_conection():
    """Accept incoming connections from clients."""
    global GAMES
    global IdCount
    IdCount = 0  # Number of people in games
    GAMES = {}  # Dictionary to track games
    while True:
        print('waiting connections')
        connection, adress = session.accept()  # Accept a connection
        print('connected to:', adress)

        start_new_thread(thread_client, (connection,))  # Start a new thread for the client


def thread_client(connection):
    """Handle a client connection."""
    global IdCount
    global GAMES
    stats = [0, 0, 0, 0]  # Stats = time playing, Wins, Loses, Ties
    while True:
        try:
            instruction = connection.recv(2048).decode()  # Receive instruction from client
            if instruction == 'Start Game':
                IdCount += 1
                playerID = 0  # [0 =pl1,1=pl2]
                gameID = (IdCount-1)//2

                if IdCount % 2 == 1:  # If IdCount is odd, assign new game
                    GAMES[gameID] = Game(gameID)
                else:  # If IdCount is even, new player == player 2
                    GAMES[gameID].ready = True  # Both players are now connected ->start game
                    playerID = 1

                game_pl_stats = inside_game_data_exchange(
                    connection, playerID, gameID)  # Exchange data with client

            elif instruction == 'Get Stats':
                connection.send(pickle.dumps(stats))  # Send stats to client
            elif instruction == 'Close Connection':
                connection.close()  # Close the connection
                break

            for i in range(3):
                stats[i] += game_pl_stats
        except:
            pass


def inside_game_data_exchange(connection, playerID, gameID):
    """Exchange game data with the client."""
    run = True
    connection.send(str.encode(str(playerID)))  # Send playerID to client
    while run:
        try:
            data = connection.recv(2048).decode()  # Receive data from client
            if gameID in GAMES:
                game = GAMES[gameID]
                if not data:
                    break
                else:
                    if data == "RESTART":  # If data is "RESTART"
                        game.winner()  # Update wins and ties
                        run = False

                    elif data != "GET GAME":  # If data is not "GET GAME"
                        game.UPDATE_CHOISE(playerID, data)  # Update player choice
                    else:
                        pass
                    connection.sendall(pickle.dumps(game))  # Send game data to client
            else:
                break
        except:  # An error on a connection could end server if this wasn't here
            break

    if playerID == 0:
        game_pl_stats = [game.wins[0], game.wins[1], game.ties]
    else:
        game_pl_stats = [game.wins[1], game.wins[0], game.ties]

    game.leave(playerID)  # Player leaves the game
    if game.end_game():  # If game ends
        del GAMES[gameID]  # Delete the game
    return game_pl_stats


create_socket()  # Create a new socket
bind_socket()  # Bind the socket
accept_conection()  # Accept connections