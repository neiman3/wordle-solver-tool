from webster import WebsterDict
import logging
import datetime

DEBUG = 1
DICT = 'dictionaries/warpeace.json'


def check_solution(letters, solution):
    if len(solution) == 0:
        return False
    result = []
    for ea in [[y[0] for y in x] for x in letters]:
        result += ea
    for word in solution:
        for letter in word:
            if letter in result:
                result.remove(letter)
    if len(result) == 0:
        return True
    return False

    # # checks to see whether all letters have been hit
    # result = []
    # for ea in [[y[1] for y in x] for x in letters]:
    #     result += ea
    # return all(result)


def update_letters(letters, pos1, pos2):
    result = []
    for i in range(4):
        side = []
        for j in range(3):
            side.append((letters[i][j][0], letters[i][j][1] + (pos1 == i and pos2 == j)))
        result.append(side)
    return result


def update_letters_by_value(letters, value):
    result = []
    for i in range(4):
        side = []
        for j in range(3):
            side.append((letters[i][j][0], letters[i][j][1] + (letters[i][j][0] == value)))
        result.append(side)
    return result


def print_box(sides_list_o):
    sides_list = [[y for y in x] for x in sides_list_o]
    SPACERS = 1
    print((" " * SPACERS).join([" "] + sides_list[0] + [" "]))
    for i in range(0, 3):
        print((" " * SPACERS).join([sides_list[3][2 - i]] + [' ', ' ', ' '] + [sides_list[1][i]]))

    sides_list[2].reverse()
    print((" " * SPACERS).join([" "] + sides_list[2] + [" "]))


def generate_solutions(letters, dictionary, max_word_length, min_word_length, max_solution_steps, pointer=None,
                       solutions=[], working_solution=[], working_word=''):

    if len(working_solution) > max_solution_steps:
        return solutions

    if len(working_word) > max_word_length:
        return solutions

    if pointer is None:
        for side in range(4):
            for letter_num in range(3):
                # Select starting letter
                pointer = dictionary.head
                starting_letter = letters[side][letter_num][0]
                if pointer.has_child(starting_letter):
                    pointer = pointer.find_child(starting_letter)
                    solutions = generate_solutions([[y for y in x] for x in letters], dictionary, max_word_length,
                                                   min_word_length, max_solution_steps, pointer=pointer,
                                                   solutions=solutions)
                logging.info("{:.1f}% complete / {} solutions found / starting letter '{}'".format(100 * (side * 3 + letter_num) / 12, len(solutions), starting_letter))
        return solutions

    working_word += pointer.value
    letter_options = get_valid_options(letters, pointer)

    if pointer.is_word and len(working_word) >= min_word_length and working_word not in working_solution:
        letters = update_letters_by_value(letters, pointer.value)
        working_solution.append(working_word)
        if dictionary.head.has_child(pointer.value):
            return generate_solutions(letters, dictionary, max_word_length, min_word_length, max_solution_steps,
                                      pointer=dictionary.head.find_child(pointer.value), solutions=solutions,
                                      working_solution=[x for x in working_solution])
        return solutions

    if check_solution(letters, working_solution):
        logging.debug("Found valid solution {}".format(working_solution))
        solutions.append(working_solution)
        return solutions

    for option in letter_options:
        if pointer.has_child(option):
            letters = update_letters_by_value(letters, pointer.value)
            solutions = generate_solutions(letters, dictionary, max_word_length, min_word_length, max_solution_steps,
                                           pointer=pointer.find_child(option), solutions=solutions,
                                           working_solution=[x for x in working_solution], working_word=working_word)
    return solutions


def get_valid_options(letters, pointer):
    letter_options = []
    side_letters = [''.join([y[0] for y in x]) for x in letters]
    for side in side_letters:
        if pointer.value not in side:
            letter_options += [x for x in side]
    return letter_options


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Letter boxed solver")

    max_word_length = 18
    min_word_length = 3
    max_solution_steps = 5

    # time calculation
    start_time = datetime.datetime.now()


    # Character entry
    letters = []
    while True:
        if not DEBUG:
            entry = input(
                "Enter all characters, with or without spaces\n(clockwise, starting from top left corner)\n > ")
        if DEBUG:
            entry = 'svc aer wmd yli'
        entry = entry.replace(" ", "")
        if len(entry) != 12:
            print("Invalid entry\n")
            continue

        # Split box into sides
        for i in range(0, 4):
            letters.append([x for x in entry[i * 3:((i + 1) * 3)]])
        print_box(letters)
        if DEBUG or input('Ok? [y/n] > ').lower() == 'y':
            break
        print(" ")

    # load game dictionary
    print("\nLoading game dictionary...")
    mydict = WebsterDict(path_to_file=DICT)
    # prune the tree using the letters
    mydict.prune([x for x in entry])
    # check number of possible game words for today
    game_list = mydict.dump()
    # text preview of game words
    preview = 'no preview available'
    if len(game_list) >= 4:
        preview = "{}, {}...{}, {}".format(game_list[0],game_list[1], game_list[-2], game_list[-1])
    print("Loaded {} valid dictionary words({})".format(len(game_list), preview))
    del preview, game_list


    # Now make permutations
    # Expand list into tuple
    print("Generating solutions...")
    letters = [[(y, 0) for y in x] for x in letters]
    solution = generate_solutions(letters, mydict, max_word_length, min_word_length, max_solution_steps)
    solution.sort(key=len)
    td = (datetime.datetime.now() - start_time).seconds
    timestring=[]
    if td // 3600 > 0:
        timestring += ['{:d} hr'.format(td // 3600)]
    if td % 3600 != 0:
        timestring += ['[{:d} min'.format((td % 3600) // 60)]
    if td % 3600 % 60 != 0:
        timestring += ['{:d} sec'.format(td % 3600 % 60)]
        timestring = " ".join(timestring)
    print("\nSearch completed in {}".format(timestring))
    print("Found {} solutions (shortest length {})".format(len(solution), (len(solution[0]) if len(solution) > 0 else "n/a")))
    print(solution[:min(10, len(solution))])
