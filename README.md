# pygames

Two small Python games, and some of my first solo projects — built while I was learning Python and programming. I'm keeping them as a snapshot of where I started.

## Jumper (`pygame/`)
A "no-internet"-style side-scroller: dodge obstacles, arrow keys to move, space to jump; it speeds up over time.
- `jumper.py` — entry point and game loop.
- `classes.py` — `Player` and `Obstacle`.
- `visuals.py` — drawing/update helper.
- `utils/` — image assets (`dot.png`, `simple_backround.jpg`).

Run:
```bash
pip install pygame
cd pygame && python jumper.py
```

## Rock-Paper-Scissors online (`Rock-Paper-Scissors_online/`)
Two players over TCP sockets against a small server.
- `Server.py` — hosts the game (handles two clients, pickled state).
- `client.py` + `client_visuals.py` — a player.
- `Network.py` — shared client/server connection helper.
- `GAME.py` — game state (choices, wins, ties).

Run (set the server's IP on every machine via the `RPS_SERVER` env var; defaults to `127.0.0.1`):
```bash
RPS_SERVER=192.168.1.20 python Server.py      # on the host
RPS_SERVER=192.168.1.20 python client.py      # on each player
```
