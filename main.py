from game import Game
import time
from data import Data
from simulation import buildPlots, letterDistributions
from colorama import Fore

if __name__ == '__main__':
    print("Welcome to my Wordle solver. You have a few options for what mode to run the program in. First, is the\n"+
          "classic Wordle game in which you receive no help from the computer. The second is the info mode, which is\n"+
          "like the classic game except you do receive help from the computer to reach the answer quicker. Next, their\n"+
          "is the 'help' mode in which you play on your phone and enter your guess and the pattern you saw. This mode\n"+
          "is included so that you can see it work on the daily Wordle which the program has no way of knowing. And if\n"+
          "you want help of course. Finally, there is a 'plots' mode that will simulate 500 Wordle games for the top 100\n"+
          "start words but I highly discourage this because you will be waiting a while. Enter 'classic', 'info', 'help',\n"+
          "or 'plots' when you are ready.")
    mode = ""
    while mode != "classic" and mode != "info" and mode != "help" and mode != "plots":
        mode = input("Mode:").lower()
        if mode == "classic":
            game = Game()
            game.playClassic()
        elif mode == "info":
            game = Game()
            game.playWithInfo()
        elif mode == "help":
            print("In this mode the program will help you solve the daily Wordle online. To use it, will prompt you to\n"+
                  "enter your guess with the 'Guess:'. Make sure to enter the guess in all-caps. Once you enter your\n"+
                  "most recent guess, it will prompt you to enter the pattern you saw with that guess. This program \n"+
                  "encodes patters using 0's, 1's, and 2's for gray, yellow, and green respectively. So if the pattern\n"+
                  "you saw was gray, gray, yellow, gray, green, then you should enter 00102. Once you've entered a \n"+
                  "guess and the pattern you saw, you will be given a list of suggested guesses where for each guess\n"+
                  "you are given the amount of information you can expect to gain from that guess and the probability\n"+
                  "of that guess being the answer. Once the program narrows it down sufficiently, it will exit and tell\n"+
                  "you what the likely answer is.")
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
        else:
            print("Please enter 'classic', 'info', 'help', or 'plots")
            time.sleep(2)
            print("\033[A                                         \033[A")
            print("\033[A                                         \033[A")