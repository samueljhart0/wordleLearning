"""
Utility file for storing functions for project
"""

import math
import random
# from colorama import init, Fore, Back

def create_dict(list) -> dict[str, bool]:
    dict = {}
    for x in list:
        dict[x] = True
    return dict

# def printAsKeyboard(dict) -> None:
#     firstRow  = "Q W E R T Y U I O P "
#     secondRow = " A S D F G H J K L  "
#     thirdRow  = "  Z X C V B N M     "
#     for f in firstRow:
#         if f == " ":
#             continue
#         else:
#             info = dict[f]
#             if info == "b":
#                 firstRow = firstRow.replace(f"{f} ", Fore.BLACK + "  ")
#             elif info == "G":
#                 firstRow = firstRow.replace(f"{f} ", Fore.GREEN + f"{f} ")
#             elif info == "Y":
#                 firstRow = firstRow.replace(f"{f} ", Fore.YELLOW + f"{f} ")
#             elif info == "B":
#                 firstRow = firstRow.replace(f"{f} ", Fore.BLACK + f"{f} ")
#     for s in secondRow:
#         if s == " ":
#             continue
#         else:
#             info = dict[s]
#             if info == "b":
#                 secondRow = secondRow.replace(f"{s} ", Fore.BLACK + "  ")
#             elif info == "G":
#                 secondRow = secondRow.replace(f"{s} ", Fore.GREEN + f"{s} ")
#             elif info == "Y":
#                 secondRow = secondRow.replace(f"{s} ", Fore.YELLOW + f"{s} ")
#             elif info == "B":
#                 secondRow = secondRow.replace(f"{s} ", Fore.BLACK + f"{s} ")
#     for t in thirdRow:
#         if t == " ":
#             continue
#         else:
#             info = dict[t]
#             if info == "b":
#                 thirdRow = thirdRow.replace(f"{t} ", "  ")
#             elif info == "G":
#                 thirdRow = thirdRow.replace(f"{t} ", Fore.GREEN + f"{t} ")
#             elif info == "Y":
#                 thirdRow = thirdRow.replace(f"{t} ", Fore.YELLOW + f"{t} ")
#             elif info == "B":
#                 thirdRow = thirdRow.replace(f"{t} ", Fore.BLACK + f"{t} ")     
#     print(f"{firstRow}\n{secondRow}\n{thirdRow}")

def buildRandList(number):
    with open("data/allowed_words.txt", "r") as f:
        guessList = list(f.read().upper().split())
    randList = random.sample(guessList, k = number)
    return randList

def listMinus(list1, list2):
    diff = []
    for obj in list1:
        if obj not in list2:
            diff.append(obj)
    return diff

def terToDec(tern):
    dec = 0
    power = 1
    for i in range(len(tern) - 1, -1, -1):
        dig = int(tern[i])
        dec += dig * power
        power *= 3
    return dec

def decToTern(dec):
    tern = ""
    while dec >= 3:
        dig = dec % 3
        tern = str(dig) + tern
        dec = dec // 3
    tern = str(dec) + tern
    return tern

def logAll(array):
    for i, a in enumerate(array):
        array[i] = log(a)
    return array

def log(number):
    if number > 0:
        return math.log2(number)
    else:
        return 0

def allowedPatterns(pattern, patterns):
    return [modAlwaysLess(pattern, p) for p in patterns]

def modAlwaysLess(pattern1, pattern2):
    while pattern1 > 1 and pattern2 > 1:
        rem1 = pattern1 % 3
        rem2 = pattern2 % 3
        if rem1 < rem2:
            return False
        pattern1 = pattern1 // 3
        pattern2 = pattern2 // 3
    return True


if __name__ == '__main__':
    patterns = dict()
    if not patterns:
        print("TRUE")