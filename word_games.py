# 1) Write a function that takes in a string as input and returns the summed value of tiles
# 2) Write a function that determines all valid rearrangements of a given string that exist in
# the SCRABBLE dictionary
# 3) GHOST loop that asks players for input using input() fn. Terminate when
# they make a scrabble world.
# ADDENDUM: Write a ghost-bot that makes the optimal play at each turn.

#You stop playing as soon as you make a word that is at least MIN_WL letters long

from anytree import Node, RenderTree

#minimum word length
MIN_WL = 4

# Should return a list of all words in the scrabble dictionary passed in at the given file path.
# Taken from last year
def LoadWords(scrabble_dictionary_path):
    file1 = open(scrabble_dictionary_path, 'r')
    Lines = []
    while True:
        line = file1.readline()
        if not line:
            break
        Lines.append(line.strip('\n'))
    return Lines[2:]

"""
Prune list to obtain all reachable words:
- length at least MIN_WL
- prefix not a word of length at least MIN_WL.
Not assuming that word_list is sorted
"""
def prune(word_list):
    my_dict = {}
    for word in word_list:
        if len(word) >= MIN_WL:
            my_dict[word] = 0
    pruned_list = []
    for word in my_dict:
        for i in range(MIN_WL, len(word)):
            if word[:i] in my_dict:
                my_dict[word]=-1
        if my_dict[word] == 0:
            pruned_list.append(word)
    pruned_list.sort()
    return pruned_list

"""
Generates all valid prefixes.
"""
def prefixes(pruned_list):
    prefix_set = set()
    for word in pruned_list:
        for i in range(len(word)+1):
            prefix_set.add(word[:i])
    prefix_list=list(prefix_set)
    prefix_list.sort()
    return prefix_list

"""
Get letters from players to build word. If player gives invalid input, allow
the player another attempt to get it right.
"""
def get_letter(current_prefix, curr_player, prefix_list):
    while True:
        letter = input("Player " + str(curr_player) +
        ", type a letter: ")
        if len(letter) == 1:
            candidate = current_prefix + letter
            if candidate not in prefix_list:
                print(candidate + " is not a valid prefix. Try again.")
            else:
                print("The word so far is " + candidate)
                return letter
        else:
            print("Enter a single uppercase letter. Try again.")

"""
Let users play game. Identify current player and winner.
"""
def ghost(pruned_list, prefix_list):
    curr_player=1
    build_word = get_letter("", curr_player, prefix_list)
    while build_word not in pruned_list:
        curr_player+=1
        build_word += get_letter(build_word, curr_player, prefix_list)
        if curr_player == 2:
            curr_player = 0
    curr_player+=1
    if curr_player == 0:
        curr_player = 2
    print(build_word)
    print("Winner: Player " + str(curr_player))



# Called from command line like "word_games.py scrabble.txt"
if __name__ == '__main__':
  scrabble_dict_path = "/Users/katherinetung/word_games/scrabble.txt"
  all_words = LoadWords(scrabble_dict_path)
  pruned_words=prune(all_words)
  prefix_words=prefixes(pruned_words)
  ghost(pruned_words, prefix_words)


