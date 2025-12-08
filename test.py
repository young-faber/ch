import random

all = input()

words = [] 

for letter in all:
    if letter in '1234567890.':
        words: str = words.remove(letter)


while 1:
    input()
    word = random.choice(words)
    for letter in word:
        if letter in '1234567890.':
            word:str = word.remove(letter)
    print(word)
    words.remove(word)

