'''
Created on Feb 15, 2020

@author: Nick
'''

import requests
import json
from mypy.types import NoneType

def left_context(word):
    """This function is used to find the left_context to the word."""
    
    request = requests.get("https://api.datamuse.com/words?md=s&lc=" + word)
    if request:
        data = json.loads(request.text)
        if len(haiku) == 1 or len(haiku) == 3: #if-elif-elif used to check length of the haiku to generate proper word based on
            for lines in data:                  #number of syllables (numSyllables)
                if lines["numSyllables"] == 2:
                    word = lines["word"]
                    return word
                else:
                    continue
        elif len(haiku) == 2 or len(haiku) == 5:
            for lines in data:
                if lines["numSyllables"] == 3:
                    word = lines["word"]
                    return word
                else:
                    continue
        elif len(haiku) == 4 or len(haiku) == 6:
            word = rhyme_word(word, haiku[1])
            return word
    else:     
        print("Sorry, connection to Datamus was unsuccessful. (Error: " + str(request.status_code) + ")")
            


def trigger_word(word):
    """This function finds the proper trigger word for the topic."""
    request = requests.get("https://api.datamuse.com/words?md=s&rel_trg=" + word)
    if request:
        data = json.loads(request.text)
        for lines in data:
            if lines["numSyllables"] == 3:
                word = lines["word"]
                return word
            else:
                continue
    else:
        print("Sorry, connection to Datamuse was unsuccessful. (Error: " + str(request.status_code) + ")")
        return word
    
def rhyme_word(word, rhyme):
    """This function is used to find a rhyme word. Works in conjunction with the left_context function. 
    (Yes I made the rhyme docstring rhyme)
    """
    request = requests.get("https://api.datamuse.com/words?md=s&lc=" + word + "&rel_rhy=" + rhyme) 
    if request:
        data = json.loads(request.text) 
        for lines in data:                  #Finds the rhyming word and the proper amount of syllables
            if lines["numSyllables"] == 2:
                if lines["word"] in haiku:
                    continue
                else:
                    word = lines["word"]
                    return word
    else:
        print("Sorry, connection to Datamuse was unsuccessful. (Error: " + str(request.status_code) + ")")
def main():
    """Main haiku program."""
    global haiku 
    haiku = []
    gate = "yes"
    print("Welcome to the haiku generator")
    while gate.lower() == "yes":            #Keeps user in the program until finished
        haiku.clear()
        word = input("Please enter a word: ")
        word = trigger_word(word)  #Finds the first word for the haiku
        haiku.append(word)
        for i in range(1,7):                 #Recycles the word variable to generate each word after the trigger word
            word = left_context(haiku[i-1])  #Iterates over the haiku list to generate the last 6 words.

            haiku.append(word)
            if None in haiku:                                  #If a NoneType pops up (meaning it couldn't find a word), then message states
                print("Sorry, a haiku could not be generated") #that the haiku can't be generated.
                break
        
        if None not in haiku:      #Assuming there is no NoneType in the list, the haiku prints out.
            print(haiku[0],haiku[1] + "\n" + haiku[2],haiku[3],haiku[4] + "\n" + haiku[5],haiku[6])
        
        gate = input("Would you like to generate another haiku? (yes/no): ")




if __name__ == "__main__":
    main()