# word contains letter
def duplicate_letters(word):
    # returns list of all letters that appear more than once in a word in form (letter, index)
    res = []
    for i in range(len(word)):
        letter = word[i]
        if word_contains(word, letter) > 1:
            # if not res:
            res.append((letter, (i)))
            # else:
            #     for j in range(len(res)):
            #         res[res.index(letter)][2].append(j)

    if not res:
        return None
    else:
        return res


def word_contains(word, letter):
    # counts number of instances of letter in word
    count = 0
    for l in word:
        if l == letter:
            count += 1
    return count


def remove_words(word, score, possible_words):
    # remove words based on score. returns new list of possible words

    for i in range(0, 5):
        letter = word[i]

        if score[i] == ' ':
            # remove all words containing that letter
            # if a duplicate is marked as gray, then check if the other duplicate is marked gray too

            skip_deletion = False

            duplicates = duplicate_letters(word)

            if duplicates is not None:
                duplicates = [l for l in duplicate_letters(word) if l[0] == letter]
                for dup in duplicates:
                    if dup[1] != ' ':
                        skip_deletion = True
                        break
                        # if any duplicate in this word is not grayed out, skip the deletion

            if not skip_deletion:
                for j in range(0, len(possible_words)):
                    if possible_words[j] is None:
                        # skip none words that may have already been removed
                        continue
                    if possible_words[j][0] == word:
                        # delete the word that was guessed
                        possible_words[j] = None
                    elif letter in possible_words[j][0]:
                        # delete all words that contain the letter:
                        possible_words[j] = None

            #
            # for j in range(0, len(possible_words)):
            #     if possible_words[j] is None:
            #         continue
            #     if possible_words[j][0] == word:
            #         possible_words[j] = None
            #     elif letter in possible_words[j][0]:
            #         possible_words[j] = None


        elif score[i] == '*':
            # can unconditionally delete words not containing letter
            for j in range(0, len(possible_words)):
                if possible_words[j] is None:
                    # skip error words
                    continue
                else:
                    if possible_words[j][0] == word:
                        # deleete guessed word
                        possible_words[j] = None
                    elif not (letter in possible_words[j][0]):
                        # delete word if it does not contain yellow letter
                        possible_words[j] = None
                    elif letter == possible_words[j][0][i]:
                        # delete words that have yellow
                        possible_words[j] = None


        elif score[i] == "!":
            # remove all words not containing that letter at that position

            # check duplicates
            # skip_deletion = False
            # duplicates = [l for l in duplicate_letters(word) if l[0] == letter]
            #
            # if duplicates is not None:
            #     for dup in duplicates:
            #
            for j in range(0, len(possible_words)):
                if possible_words[j] is None:
                    continue
                if possible_words[j][0] == word:
                    possible_words[j] = None
                elif possible_words[j][0][i] != letter:
                    possible_words[j] = None
    # clean list
    possible_words = [item for item in possible_words if item is not None]
    return possible_words
