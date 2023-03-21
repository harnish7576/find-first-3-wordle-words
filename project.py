# Importing libraries
import pandas as pd
import numpy as np
# import random

# ------------------------------------------------------------
# Computing letter frequency thorughout the word list.
def letter_freq(words):
    freqs = [0]*26
    for word in words:
        for char in word:
            freqs[ord(char)-97] += 1
    
    char_freq_hashmap = {}
    for ord_val in range(97, 123):
        char_freq_hashmap[chr(ord_val)] = freqs[ord_val-97]
    # print(freqs)
    return char_freq_hashmap

# ------------------------------------------------------------
# Computing number of vowels in each word.
def vowel_freq(words):
    vowel_map = {}
    for word in words:
        vowel_count = 0
        for char in word:
            if char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u':
                vowel_count += 1

        if vowel_count in vowel_map:
            vowel_map[vowel_count].append(word)
        else: vowel_map[vowel_count] = [word]
    return vowel_map

# ------------------------------------------------------------
# Computing Monograms of each word.
def find_monograms(words):
    monograms_list = []
    for word in words:
        monograms_list.append(list(word))
    # print(monograms_list)
    return monograms_list

# ------------------------------------------------------------
# Computing Bigrams of each word.
def find_bigrams(words):
    bigrams_list = []
    for word in words:
        bigram = []
        for idx in range(0,4): # idx: 01 12 23 34
            bigram.append(word[idx:idx+2])
        bigrams_list.append(bigram)
    # print(bigrams_list)
    return bigrams_list

# ------------------------------------------------------------
# Computing chance of a word.
# For example, “hunch” is ( the chance of word starting with the
# letter “h”, plus the chance of “hu”, plus the chance of “un”, 
# plus the chance of “nc”, plus the chance of “ch”, plus the 
# chance of a word ending in “h”) all divided by 6 transitions. 
def find_chance(word, no_of_words, bigrams_list, no_of_bigrams, first_idx_freqs, last_idx_freqs):
    chance = 0
    chance += (first_idx_freqs[ord(word[0])-97]/no_of_words)

    for idx in range(0,4):
        count_of_two_letter = 0
        # print(word[idx:idx+2])
        for bigram in bigrams_list:
            if word[idx:idx+2] in bigram:
                count_of_two_letter += 1
        # if idx == 1: print(count_of_two_letter)
        chance += (count_of_two_letter/no_of_bigrams)
    
    chance += (last_idx_freqs[ord(word[4])-97]/no_of_words)
    chance /= 6
    return chance

# ------------------------------------------------------------
# Computing frequency of each character in the 
# first index and the last index.
def find_letter_freq_first_last_idx(words):
    first_idx_freqs = [0]*26
    last_idx_freqs = [0]*26
    for word in words:
        first_idx_freqs[ord(word[0])-97] += 1
        last_idx_freqs[ord(word[4])-97] += 1
    return first_idx_freqs, last_idx_freqs

# ------------------------------------------------------------
# Computing Cost Function.
# Total of frequency of first letter of word being in 
# the first place and frquency of each character of 
# the word in the word list.
def cost_function(word, first_idx_freqs, letter_freqs):
    cost = 0
    cost += first_idx_freqs[ord(word[0])-97]
    for char in word:
        cost += letter_freqs[char]
    return cost

# ------------------------------------------------------------
def main():

    print()
    # Reading File
    words = []
    with open('wordle_words.txt', 'r') as file:
        for line in file:
            words.append(line)
    words = [word.strip() for word in words]

    # Generating a random word for the Wordle of the Day 
    # guess_word = random.choice(words)
    # print("Wordle word: ", guess_word)


    letter_freqs = letter_freq(words)
    monograms_list = find_monograms(words)
    bigrams_list = find_bigrams(words)

    no_of_words = len(words)
    no_of_bigrams = 4*len(words)

    first_idx_freqs, last_idx_freqs = find_letter_freq_first_last_idx(words)

    print("----------------------------First Guess-----------------------------")
    # Computing the chance of the words occuring
    chance_of_words = {}
    for word in words:
        chance_of_words[word] = find_chance(word, no_of_words, bigrams_list, no_of_bigrams, first_idx_freqs, last_idx_freqs)
    
    # Sorting in Descending order of Chance of Words 
    sorted_chance_of_words = sorted(chance_of_words.items(), key=lambda x:x[1], reverse=True)
    
    # Cost Function breaking a tie, if there is one
    if sorted_chance_of_words[0][1] == sorted_chance_of_words[1][1]:
            print("There was a tie for the best word for the First Guess")
            if cost_function(sorted_chance_of_words[0][0], first_idx_freqs, letter_freqs) > cost_function(sorted_chance_of_words[1][0], first_idx_freqs, letter_freqs):
                first_guess = sorted_chance_of_words[0][0]
                print("First Guess: ", sorted_chance_of_words[0][0])
            else:
                first_guess = sorted_chance_of_words[1][0]
                print("First Guess: ", sorted_chance_of_words[1][0])
    else: 
        print("There was no tie for the Best Word for the First Guess")
        first_guess = sorted_chance_of_words[0][0]
        print("First Guess: ", sorted_chance_of_words[0][0])
    print()

    # Top 20 
    print("Top 20 best words for the First Guess: ")
    for idx in range(0,21):
        print(sorted_chance_of_words[idx][0])
    print("---------------------------------------------------------------------")

    print()

    print("----------------------------Second Guess-----------------------------")
    # Computing subset of words who don't have letters that are in the first word
    second_guess_words = []
    for word in words:
        # excluding words with duplicate letters
        if len(word) == len(set(word)):
            if not set(word).intersection(set(first_guess)): second_guess_words.append(word)

    # Computing the chance of the words occuring
    chance_of_words = {}
    for word in second_guess_words:
        chance_of_words[word] = find_chance(word, no_of_words, bigrams_list, no_of_bigrams, first_idx_freqs, last_idx_freqs)

    # Sorting in Descending order of Chance of Words 
    sorted_chance_of_words = sorted(chance_of_words.items(), key=lambda x:x[1], reverse=True)

    # Cost Function breaking a tie, if there is one
    if sorted_chance_of_words[0][1] == sorted_chance_of_words[1][1]:
            print("There was a tie for the best word for the Second Guess")
            if cost_function(sorted_chance_of_words[0][0], first_idx_freqs, letter_freqs) > cost_function(sorted_chance_of_words[1][0], first_idx_freqs, letter_freqs):
                second_guess = sorted_chance_of_words[0][0]
                print("Second Guess: ", second_guess)
            else:
                second_guess = sorted_chance_of_words[1][0]
                print("Second Guess: ", second_guess)
    else: 
        print("There was no tie for the Best Word for the Second Guess")
        second_guess = sorted_chance_of_words[0][0]
        print("Second Guess: ", second_guess)
    print()

    # Top 20 
    print("Top 20 best words for the Second Guess: ")
    for idx in range(0,21):
        print(sorted_chance_of_words[idx][0])
    print("---------------------------------------------------------------------")

    print()

    print("----------------------------Third Guess------------------------------")
    # Computing subset of words who don't have letters that are in the first and the second word
    third_guess_words = []
    for word in second_guess_words:
        # excluding words with duplicate letters
        if len(word) == len(set(word)):
            if not set(word).intersection(set(second_guess)): third_guess_words.append(word)

    # Computing the chance of the words occuring
    chance_of_words = {}
    for word in third_guess_words:
        chance_of_words[word] = find_chance(word, no_of_words, bigrams_list, no_of_bigrams, first_idx_freqs, last_idx_freqs)

    # Sorting in Descending order of Chance of Words
    sorted_chance_of_words = sorted(chance_of_words.items(), key=lambda x:x[1], reverse=True)

    # Cost Function breaking a tie, if there is one
    if sorted_chance_of_words[0][1] == sorted_chance_of_words[1][1]:
            print("There was a tie for the best word for the Third Guess")
            if cost_function(sorted_chance_of_words[0][0], first_idx_freqs, letter_freqs) > cost_function(sorted_chance_of_words[1][0], first_idx_freqs, letter_freqs):
                third_guess = sorted_chance_of_words[0][0]
                print("Third Guess: ", third_guess)
            else:
                third_guess = sorted_chance_of_words[1][0]
                print("Third Guess: ", third_guess)
    else: 
        print("There was no tie for the Best Word for the Third Guess")
        third_guess = sorted_chance_of_words[0][0]
        print("Third Guess: ", third_guess)
    print()

    # Top 20 
    print("Top 20 best words for the Third Guess: ")
    for idx in range(0,len(sorted_chance_of_words)):
        print(sorted_chance_of_words[idx][0])
    print("---------------------------------------------------------------------")

if __name__ == '__main__':
    main()


