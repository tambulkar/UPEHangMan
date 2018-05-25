import requests
import re
import random
import operator

#dict = {}
#with open('./dictionary.txt','r') as inf:
#    dict = eval(inf.read())

dict = {}
for line in open('./dictionary2.txt','r').readlines():
    wordList = open('./dictionary2.txt','r').readlines()
    if((len(line)-1) in dict.keys()):
        dict[len(line)-1].append(line[:-1])
    else:
        dict[len(line)-1] = [line[:-1]]


alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def randomLetterGenerator():
    letter = random.choice(alphabet)
    alphabet.remove(letter)
    return letter

def findCandidates(regex, list):
    reg = re.compile(regex)
    return filter(reg.match,list)

def findMostComLetter(candidates):
    letterCount = {}
    for word in candidates:
        for letter in word:
            if(letter in alphabet):
                if(letter in letterCount.keys()):
                    letterCount[letter] = letterCount[letter] + 1
                else:
                    letterCount[letter] = 1
    print(candidates)
    print(letterCount)
    return max(letterCount.items(), key=operator.itemgetter(1))[0]



#Start Game
r = requests.get("http://upe.42069.fun/7GBQY")
#sentence = r.json()["state"]
#sentence = re.sub('[^_ a-z]', '', sentence)
#sentence = sentence.replace("_",".")

r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "e"})
alphabet.remove("e")
r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "t"})
alphabet.remove("t")
r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "a"})
alphabet.remove("a")
r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': "s"})
alphabet.remove("s")

while(r.json()["status"] == "ALIVE"):
    sentence = r.json()["state"]
    sentence = re.sub('[^_ a-z]', '', sentence)
    sentence = sentence.replace("_", ".")
    words = sentence.split(" ")
    for word in words:
        if('.' not in word):
            words.remove(word)
    longestWord = max(words, key=len)
    candidates = list(findCandidates(longestWord, dict[len(longestWord)]))
    randLetter = findMostComLetter(candidates)
    alphabet.remove(randLetter)
    r = requests.post('http://upe.42069.fun/7GBQY', data = {'guess': randLetter})
    print(r.json())
