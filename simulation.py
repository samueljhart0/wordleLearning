import numpy as np
from game import ANSWER_FILE, Game
from tqdm import tqdm
from data import WORD_FILE, Data
import itertools as it
import random
import matplotlib.pyplot as plt
from colorama import init
from  matplotlib.colors import LinearSegmentedColormap

"""
This file holds functions that were used to build the plots in the poster and report. These are the functions run in
the 'plots' mode.
"""

def letterDistributions():
    """
    Builds letter/position heatmaps and saves them in the plots directory.
    """
    with open(WORD_FILE, 'r') as f:
        answerList = list(f.read().upper().split())
    
    letters = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    engFreq = np.array([0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406,
                        0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074])
    engInd = np.argsort(engFreq)[::-1]
    alphabet = dict(zip(letters, it.count()))
    heatMap = np.zeros((26,5))
    letterBuckets = np.zeros(26)
    for word in answerList:
        for i, l in enumerate(word):
            heatMap[alphabet[l]][i] += 1
            letterBuckets[alphabet[l]] += 1
    byLetter = heatMap / heatMap.sum(1).reshape(-1,1)
    byPosition = heatMap / heatMap.sum(0).reshape(1,-1)
    letterFreq = letterBuckets / letterBuckets.sum()
    wordleInd = np.argsort(letterFreq)[::-1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(letters[engInd], engFreq[engInd], color='green')
    plt.ylabel('Frequency')
    fig.tight_layout()
    plt.savefig("plots/engFreq", dpi=300, bbox_inches="tight")

    cmap=LinearSegmentedColormap.from_list('bg',["gold", "green"], N=256)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(byLetter, cmap=cmap)
    plt.colorbar(im)
    ax.set_xticks(np.arange(5), labels=[1,2,3,4,5])
    ax.set_yticks(np.arange(26), labels=letters)
    plt.setp(ax.get_xticklabels(), ha="center")
    ax.set_title("Letter Distributions Over Positions")
    fig.tight_layout()
    plt.savefig("plots/byLetter", dpi=300, bbox_inches="tight")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(byPosition, cmap=cmap)
    plt.colorbar(im)
    ax.set_xticks(np.arange(5), labels=[1,2,3,4,5])
    ax.set_yticks(np.arange(26), labels=letters)
    plt.setp(ax.get_xticklabels(), ha="center")
    ax.set_title("Position Distributions Over Letters")
    fig.tight_layout()
    plt.savefig("plots/byPostion", dpi=300, bbox_inches="tight")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(letters[wordleInd], letterFreq[wordleInd], color='green')
    plt.ylabel('Frequency')
    fig.tight_layout()
    plt.savefig("plots/wordleFreq", dpi=300, bbox_inches="tight")
    

def simulateAll(guessList):
    """
    Simulates 500 games starting from each of the words in the guessList parameter.
    """
    random.seed(123)
    dataStore = dict()
    dataStore["wordsToIndex"] = dict(zip(guessList, it.count()))
    dataStore["avg"] = np.zeros(len(guessList))
    dataStore["buckets"] = np.zeros((len(guessList), 10))

    with open(ANSWER_FILE, "r") as f:
        answerList = random.sample(list(f.read().upper().split()), 500)
    
    for guess in guessList:
        guessBuckets = [0 for _ in range(10)]
        print(f"Start Word:{guess}")
        numerator = 0
        denominator = 0
        avg = 1
        for i in tqdm(range(len(answerList)), ncols=100, leave=True):
        # for i in range(len(answerList)):
            answer = answerList[i]
            game = Game(answer)
            trial = game.simulate(guess)
            guessBuckets[trial - 1] += 1
            numerator += trial
            denominator += 1
            avg = numerator / denominator
        idx = dataStore["wordsToIndex"][guess]
        dataStore["avg"][idx] = avg
        dataStore["buckets"][idx] = guessBuckets
        print(f"Avg # of guesses to answer:{avg}")
    return dataStore

def buildPlots():
    """
    Builds the histograms from the simulated games.
    """
    # Candidate words are those of the top 100 starting entropy
    data = Data("DUMMY")
    candidates = []
    top = data.giveTop(100)
    for row in top:
        candidates.append(row[0])

    # Simulate these and plot their histograms and display their averages
    allData = simulateAll(candidates)
    averages = allData["avg"]
    
    # Get the best 2 and then add the popular starting words
    wordsToPlot = np.argsort(averages)[:6]

    # Change last 4 indices to those of the popular starting words
    wordsToPlot[2] = allData["wordsToIndex"]["ARISE"]
    wordsToPlot[3] = allData["wordsToIndex"]["ADIEU"]
    wordsToPlot[4] = allData["wordsToIndex"]["CRATE"]
    wordsToPlot[5] = allData["wordsToIndex"]["SOARE"]
    for idx in wordsToPlot:
        word = candidates[idx]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xticks(np.arange(10), labels=[1,2,3,4,5,6,7,8,9,10])
        plt.bar(np.arange(10), allData["buckets"][idx], color='green')
        plt.title(f"{word} Histogram | Avg: {averages[idx]}")
        plt.ylabel('# of games')
        plt.xlabel('# of guesses to get answer')
        fig.tight_layout()
        plt.savefig(f"plots/{word}histogram", dpi=300, bbox_inches="tight")


