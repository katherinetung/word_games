# 1) Write a function that takes in a string as input and returns the summed value of tiles
# 2) Write a function that determines all valid rearrangements of a given string that exist in
# the SCRABBLE dictionary
# 3) GHOST loop that asks players for input using input() fn. Terminate when
# they make a scrabble world.
# ADDENDUM: Write a ghost-bot that makes the optimal play at each turn.

#You stop playing as soon as you make a word that is at least MIN_WL letters long

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
    mydict = {}
    for word in word_list:
        if len(word) >= MIN_WL:
            mydict[word] = 0
    pruned_list = []
    for word in mydict:
        for i in range(MIN_WL, len(word)):
            if word[:i] in mydict:
                mydict[word]=-1
        if mydict[word] == 0:
            pruned_list.append(word)
    pruned_list.sort()
    return pruned_list

"""
Let users play game. Identifies winner. TODO: catch fake words.
"""
def ghost(pruned_list):
    curr_player=1
    build_word = input("Player " + str(curr_player) + ", type a letter: ")
    while build_word not in pruned_list:
        curr_player+=1
        build_word += input("Player " + str(curr_player) + ", type a letter: ")
        if curr_player == 2:
            curr_player = 0
    if curr_player == 0:
        curr_player = 2
    print(build_word)
    print("Winner: Player " + str(curr_player))


# Called from command line like "word_games.py scrabble.txt"
if __name__ == '__main__':
  scrabble_dict_path = "/Users/katherinetung/word_games/scrabble.txt"
  all_words = LoadWords(scrabble_dict_path)
  pruned_words=prune(all_words)
  ghost(pruned_words)


