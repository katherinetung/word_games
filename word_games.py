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
    my_dict = {}
    for word in word_list:
        if len(word) >= MIN_WL:
            my_dict[word] = 0
    pruned_dict = {}
    for word in my_dict:
        for i in range(MIN_WL, len(word)):
            if word[:i] in my_dict:
                my_dict[word]=-1
        if my_dict[word] == 0:
            pruned_dict[word] = 0
    return pruned_dict

"""
Generates all valid prefixes as dictionary. Key:value is prefix:-1.
"""
def prefixes(pruned_dict):
    prefix_dict = {}
    for word in pruned_dict:
        for i in range(len(word)+1):
            prefix_dict[word[:i]]=-1
    return prefix_dict

"""
Get letters from players to build word. If player gives invalid input, allow
the player another attempt to get it right.
"""
def get_letter(current_prefix, curr_player, prefix_dict):
    while True:
        letter = input("Player " + str(curr_player) +
        ", type a letter: ")
        if len(letter) == 1:
            candidate = current_prefix + letter
            if candidate not in prefix_dict:
                print(candidate + " is not a valid prefix. Try again.")
            else:
                print("The word so far is " + candidate)
                return letter
        else:
            print("Enter a single uppercase letter. Try again.")

"""
Compute game value of a prefix (number of turns before game ends).
For example, game value of "L" is 4 (2nd player can force end result "LLAMA")
"""
def game_value(prefix, prefix_dict, word_dict):
    if not prefix_dict[prefix] == -1:
        return prefix_dict[prefix]
    if prefix in word_dict:
        prefix_dict[prefix] = 0
        return prefix_dict[prefix]
    is_winner = False
    best_so_far = 0
    for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        child = prefix+str(a)
        if child in prefix_dict:
            child_value = game_value(child, prefix_dict, word_dict)
            winner_child = child_value%2 == 0
            if is_winner:
                if not winner_child:
                    best_so_far = min(best_so_far, 1 + child_value)
            else:
                if not winner_child:
                    is_winner = True
                    best_so_far = 1 + child_value
                else:
                    best_so_far = max(best_so_far, 1 + child_value)
    prefix_dict[prefix] = best_so_far
    return prefix_dict[prefix]

"""
Find an optimal next letter to play.
"""
def recommended_play(prefix, prefix_dict, word_dict):
    if prefix in word_dict:
        return ""
    is_winner = game_value(prefix, prefix_dict, word_dict) % 2 == 0
    best_candidate = ""
    best_value = 0
    for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        child = prefix+str(a)
        if child in prefix_dict:
            child_value = game_value(child, prefix_dict, word_dict)
            parent_value = game_value(prefix, prefix_dict, word_dict)
            if child_value == parent_value - 1:
                return str(a)
    print(prefix + "utter failure in recommended play. We're no strangers to...")

def playable_letters_game_values(prefix, prefix_dict, word_dict):
    message=""
    for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        child = prefix+str(a)
        if child in prefix_dict:
            g_value = str(game_value(child, prefix_dict, word_dict))
            message = message + str(a) + ":" + g_value + " "
    return message

"""
Dtermine playable letters.
"""
def playable_letters(prefix, prefix_dict, word_dict):
    message="Your options are: "
    for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        child = prefix+str(a)
        if child in prefix_dict:
            g_value = str(game_value(child, prefix_dict, word_dict))
            message = message + str(a) + " "
    return message

"""
Let users play game. Identify current player and winner.
"""
def ghost_2_player(prefix_dict, word_dict):
    curr_player=1
    build_word = get_letter("", curr_player, prefix_dict)
    while build_word not in word_dict:
        curr_player+=1
        build_word += get_letter(build_word, curr_player, prefix_dict)
        if curr_player == 2:
            curr_player = 0
    curr_player+=1
    if curr_player == 0:
        curr_player = 2
    print(build_word)
    print("Winner: Player " + str(curr_player))

"""
Play against computer which goes 2nd. Identify current player and winner.
"""
def ghost_1_player(prefix_dict, word_dict):
    curr_player=1
    build_word = get_letter("", curr_player, prefix_dict)
    while build_word not in word_dict:
        curr_player+=1
        if curr_player == 1:
            build_word += get_letter(build_word, curr_player, prefix_dict)
            if build_word in word_dict:
                print("Computer won.")
        if curr_player == 2:
            build_word += recommended_play(build_word, prefix_dict, word_dict)
            print("The computer made " + build_word)
            curr_player = 0
            if build_word not in word_dict:
                print(playable_letters(build_word, prefix_dict, word_dict))
            else:
                print("You won!")

"""
Select the 1 player or 2 player version depending on user input."
"""
def game_version(prefix_dict, word_dict):
    version = input("For 1 player version, type '1'\nFor 2 player version, type '2'\n")
    if version == '1':
        ghost_1_player(prefix_dict, word_dict)
    elif version == '2':
        ghost_2_player(prefix_dict, word_dict)
    else:
        print("Your input was invalid.")
        exit()



# Called from command line like "word_games.py scrabble.txt"
if __name__ == '__main__':
  scrabble_dict_path = "/Users/katherinetung/word_games/scrabble.txt"
  all_words = LoadWords(scrabble_dict_path)
  pruned_words=prune(all_words)
  prefix_words=prefixes(pruned_words)
  game_version(prefix_words, pruned_words)


