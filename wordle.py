# from wordle_obj import *
from word_test import *
from word_freq import *


def rescore(list_of_words):
    fn = ".wordle_temp.txt"
    f = open(fn, 'w')
    list_of_words = [str(i[0]) + '\n' for i in list_of_words]
    f.writelines(list_of_words)
    f.close()
    freqdata = frequency_analysis(fn)
    returndict = build_dict(fn, freqdata)
    return sorted(returndict, key=lambda x: x[1])


def frequency_analysis(filename, chars="letters.txt"):
    res = []
    c = open(chars, 'r')
    for line in c:
        res.append([line[0].lower(), 0])
    c.close()

    f = open(filename, 'r')

    for line in f:
        for letter in line:
            if letter == '\n':
                pass
            for i_entry in range(len(res)):
                if res[i_entry][0] == letter.lower():
                    res[i_entry][1] = res[i_entry][1] + 1
                    break
    f.close()
    return res


def build_dict(file, freq_data):
    # word(str), overall_score(int), freq_score, num_unique_vowels(int)
    res = []
    f = open(file, 'r')
    for line in f:
        if line[-1] == '\n':
            word = line[:-1]
        else:
            word = line

        freq_score = get_freq_score(word, freq_data)
        vowel_score = get_vowel_score(word)
        oxford_score = get_oxford_score(word, oxford)
        res.append([word, freq_score * (vowel_score) * oxford_score, freq_score, vowel_score])

    return res


def get_freq_score(word, freq_data_scoring):
    score = 0
    already = []
    for letter in word:
        if letter in already:
            pass
        for i in range(0, len(freq_data_scoring)):
            if freq_data_scoring[i][0] == letter:
                score += freq_data_scoring[i][1]
                already.append(letter)
                pass

    if duplicate_letters(word) is None:
        return score
    else:
        return score / (len(duplicate_letters(word)) + 1)


def get_vowel_score(word):
    return 1
    score = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    already = []
    for letter in word:
        if letter in vowels:
            if letter not in already:
                score += 1
                already.append(letter)
    return score


def get_oxford_score(word, oxford):
    if word in oxford:
        return 2
    else:
        return 1


freq_data = frequency_analysis("dictionaries/wordle_game_dictionary.txt")
oxford = oxford_list()
dict = build_dict("dictionaries/wordle_game_dictionary.txt", freq_data)

possible_words = sorted(dict, key=lambda x: x[1])

# starting word
shown_starting_words = 0
show_help = 1
correct = False

print("Welcome to Wordle Helper! Enter your starting word. Press enter to see good starting words.")


def prompt_word(shown, dict):
    print("Enter your word")
    ctl = input('> ')
    if ctl == '':
        if len(dict) <= 10:
            for word in dict:
                print(word[0], "   vowels:", word[3], "   score:", word[1])
        else:
            for word in dict[len(dict) - shown - 10:len(dict) - shown]:
                print(word[0], "   vowels:", word[3], "   score:", word[1])
        shown += 10
        return prompt_word(shown, dict)
    else:
        if len(ctl) != 5:
            print("Error: not a 5 letter word")
            return prompt_word(shown, dict)
        for words in possible_words:
            if words[0] == ctl:
                return ctl
        print("Error: word not in list")
        return prompt_word(shown, dict)


def prompt_score(help=0):
    print("Word score")
    if help:
        print("[space] : not in word\n  [*]   : right letter, wrong location\n  [!]   : right letter, right location")
    ctl = input(" > ")
    if ctl == '':
        return prompt_score(1)
    if len(ctl) != 5:
        print("Error: score must be five characters")
        return prompt_score()
    for char in ctl:
        if not ((char == '*') or (char == ' ') or (char == '!')):
            print("Error: score contains unknown character")
            return prompt_score()
    return ctl


while not correct:
    if len(possible_words) == 1:
        print("Only one word remains. The solution is", possible_words[0][0])
        break
    elif len(possible_words) == 0:
        try:
            score
        except NameError:
            pass
        else:
            if score == '!!!!!':
                print("Congratulations, you solved the wordle.")
                break
        print("There may be an error with your word selection or score. No possible words remain.")
        break
    else:
        print(len(possible_words), "possible words remaining")
    word = prompt_word(0, possible_words)
    score = prompt_score(show_help)

    possible_words = remove_words(word, score, possible_words)
    possible_words = rescore(possible_words)

    # for i in range(0, 5):
    #     letter = word[i]
    #     if score[i] == ' ':
    #         # remove all words containing that letter
    #         for j in range(0, len(possible_words)):
    #             if possible_words[j] is None:
    #                 continue
    #             if possible_words[j][0] == word:
    #                 possible_words[j] = None
    #             elif letter in possible_words[j][0]:
    #                 possible_words[j] = None
    #     elif score[i] == '*':
    #         # remove all words not containing that letter
    #         for j in range(0,len(possible_words)):
    #             if possible_words[j] is None:
    #                 continue
    #             if possible_words[j][0] == word:
    #                 possible_words[j] = None
    #             elif not (letter in possible_words[j][0]):
    #                 possible_words[j] = None
    #     elif score[i] == "!":
    #         # remove all words not containing that letter at that position
    #         for j in range(0, len(possible_words)):
    #             if possible_words[j] is None:
    #                 continue
    #             if possible_words[j][0] == word:
    #                 possible_words[j] = None
    #             elif possible_words[j][0][i] != letter:
    #                 possible_words[j] = None
    #
    # # clean list
    # possible_words = [item for item in possible_words if item is not None]
