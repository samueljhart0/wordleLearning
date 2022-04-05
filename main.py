from game import Game
import time

if __name__ == '__main__':
    mode = ""
    while mode != "demo" and mode != "classic" and mode != "info":
        mode = input("Mode:").lower()
        if mode == "demo":
            game = Game("CRIMP")
            game.playClassic()
        elif mode == "classic":
            game = Game()
            game.playClassic()
        elif mode == "info":
            game = Game()
            game.playWithInfo()
        else:
            print("Please enter 'demo', 'classic' or 'info'")
            time.sleep(2)
            print("\033[A                                         \033[A")
            print("\033[A                                         \033[A")
