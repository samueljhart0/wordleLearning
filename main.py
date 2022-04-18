from game import Game
import time
from data import Data
from simulation import buildPlots, letterDistributions, simulateAll
from colorama import Fore

if __name__ == '__main__':
    mode = ""
    while mode != "demo" and mode != "classic" and mode != "info" and mode != "help" and mode != "plots":
        mode = input("Mode:").lower()
        if mode == "demo":
            game = Game("ADULT")
            game.playWithInfo()
        elif mode == "classic":
            game = Game()
            game.playClassic()
        elif mode == "info":
            game = Game()
            game.playWithInfo()
        elif mode == "help":
            data = Data()
            pattern = "00000"
            while len(data.possible) > 2:
                guess = input("Guess:")
                pattern = input("Pattern:")
                data.processInput(guess, pattern)
                print(Fore.BLACK + "WORD   E[Info]   Var[Info]  p(WORD)")
                topTen = data.giveTop(10)
                for row in topTen:
                    word, info, var, prob = row[0], row[1], row[2], row[3]
                    print(f"{word}  {round(info, 4)}     {round(var,4)}      {round(prob, 6)}")
        elif mode == "plots":
            letterDistributions()
            buildPlots()
        elif mode == "sim":
            simulateAll()
        else:
            print("Please enter 'demo', 'classic', 'info', 'help', or 'plots")
            time.sleep(2)
            print("\033[A                                         \033[A")
            print("\033[A                                         \033[A")