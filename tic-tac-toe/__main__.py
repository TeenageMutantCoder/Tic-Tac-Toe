try:
    from game import Game
except ImportError:
    from .game import Game

if __name__ == '__main__':
    Game(500)