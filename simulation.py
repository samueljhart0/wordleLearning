from game import Game
from tqdm import tqdm

def simulateAll():
    with open("data/allowed_words.txt", "r") as f:
        guessList = list(f.read().upper().split())
    with open("data/answer_words.txt", "r") as f:
        answerList = list(f.read().upper().split())
    for guess in guessList:
        print(f"Start word: {guess}")
        numerator = 0
        denominator = 0
        avg = 1
        for i in tqdm(range(len(answerList)), ncols=100, leave=True):
            # print(f"\nAvg # of guesses to answer:{avg}")
            answer = answerList[i]
            game = Game(answer)
            trial = game.simulate(guess)
            numerator += trial
            denominator += 1
            avg = numerator / denominator
        print(f"Avg # of guesses to answer:{avg}")