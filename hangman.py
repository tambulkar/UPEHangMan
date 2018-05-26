import requests
import re
import operator
import time

dict = {}
for line in open('./dictionary.txt','r').readlines():
    wordList = open('./dictionary.txt','r').readlines()
    if((len(line)-1) in dict.keys()):
        dict[len(line)-1].append(line[:-1])
    else:
        dict[len(line)-1] = [line[:-1]]


alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
freqLetters = ["e","t","a","o","i","n","s","r","h","l","d","c","u","m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]

#Reset lists every game
def resetLists():
    global alphabet
    global freqLetters
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    freqLetters = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c",
                   "u", "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j",
                   "q", "z"]

def findCandidates(regex, list):
    #Pull words from list that match regex
    reg = re.compile(regex)
    return filter(reg.match,list)

def findMostComLetter(candidates):
    #Count numebrr of letters in words
    letterCount = {}
    for word in candidates:
        for letter in word:
            if(letter in alphabet):
                if(letter in letterCount.keys()):
                    letterCount[letter] = letterCount[letter] + 1
                else:
                    letterCount[letter] = 1

    #If word doesn't exist, guess next most common letter
    if(len(letterCount) is 0):
        letter = freqLetters[0]
        return letter

    #Guess letter with highest count
    return max(letterCount.items(), key=operator.itemgetter(1))[0]


for i in range(10):
    #Reset lists at beginning of every game
    resetLists()

    #Start Game
    r = requests.get("http://upe.42069.fun/7GBQY")
    print(r.json())

    #Guess 3 most common letters
    r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "e"})
    alphabet.remove("e")
    freqLetters.remove("e")
    r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "t"})
    alphabet.remove("t")
    freqLetters.remove("t")
    r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "a"})
    alphabet.remove("a")
    freqLetters.remove("a")

    #Run the guesses until dead
    while(r.json()["status"] == "ALIVE"):
        #Split sentence into words that are regex for each word
        sentence = r.json()["state"]
        sentence = re.sub('[^_ a-z]', '', sentence)
        sentence = sentence.replace("_", ".")
        words = sentence.split(" ")

        #Remove words that have already been solved
        i = 0
        while( i < len(words)-1):
            if('.' not in words[i]):
                words.remove(words[i])
            else:
                i = i+1

        #Find longest word that hasn't been solved and find possible candidates
        longestWord = max(words, key=len)
        candidates = list(findCandidates(longestWord, dict[len(longestWord)]))

        #Guess most common letters in the candidates
        randLetter = findMostComLetter(candidates)

        #Remove guessed letter
        alphabet.remove(randLetter)
        freqLetters.remove(randLetter)

        #Make Guess request
        r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': randLetter})
        time.sleep(0.2)
        print(r.json())

    #Write new words to dictionary
    if(r.json()["status"] == "DEAD"):
        f = open('./dictionary.txt', 'a+')
        lyrics = r.json()["lyrics"].split(" ")
        for word in lyrics:
            editedWord = re.sub('[^a-z]', '', word)
            f.write(editedWord + "\n")
        f.close()

    time.sleep(1)
