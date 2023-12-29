import os
import json

INPUT_FILE = 'books/warpeace.txt'
OUTPUT_FILE = 'dictionaries/warpeace.json'
MIN_WORD_LENGTH = 3

# Text processing to form dictionary from large texts (ie books)

if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # delimiters such as apostrophe, dash, etc that would disqualify a word
    disqualifying_delimiters = ['-','–','—','\'']
    bad_chars = {}

    # open raw text file
    words = {}
    with open(INPUT_FILE) as f:
        for line in f:
            if line[0] == '#':  # comment
                continue
            if line[0] == '\n': # empty line
                continue
            line = line.lower() # lowercase
            # Scan the line for illegal characters and replace them with spaces
            for char in line:
                if not char.isalpha():
                    if char in bad_chars:
                        bad_chars[char] += 1
                    else:
                        bad_chars[char] = 1
                    if char not in disqualifying_delimiters:
                        line = line.replace(char, ' ') # replace all non-alphanumeric chars
            # Now split the line by spaces, removing any list items that are blank
            line = [x for x in line.split(' ') if x != '']
            # Remove all words that had disqualifying delimiters
            for word in line:
                if word.isalpha():
                    # Now append the main dictionary with all new words in this line
                    # This will count instances of the words
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

    # completed- write to file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(words, f)


