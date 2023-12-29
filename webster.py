import json

# DICT_FILENAME = "mit10k.json"
DICT_FILENAME= "dictionaries/letterboxed.json"
TEST_DICTIONARY = ['apple', 'ball', 'cat', 'aaab', 'bab', 'foo', 'apples']


class WebsterDict:
    #
    def __init__(self, path_to_file=DICT_FILENAME):
        self.head = Node()
        with open(path_to_file) as f:
            base_dictionary = json.load(f)
            for word in base_dictionary.keys():
                # for word in TEST_DICTIONARY:
                word = [x for x in word]
                self.head.append(word)

    def is_word(self, word, pointer=None):
        if pointer is None:
            pointer = self.head
        if type(word) is str:
            word = [x for x in word.lower()]
        if len(word) == 0:
            return pointer.is_word
        if word[0] in pointer.children:
            return self.is_word(word[1:], pointer.children[word[0]])
        return False

    def dump(self, pointer=None, result=[], my_word=''):
        if pointer is None:
            pointer = self.head
        if pointer.is_word:
            result.append(my_word)
        for child in pointer.children.keys():
            self.dump(pointer.children[child], result, my_word + child)
        result.sort()
        return result

    def prune(self, list_of_values_to_remove, pointer=None):
        # initial function call
        if pointer is None:
            self.prune(list_of_values_to_remove, self.head)
            return

        # node pruning
        children = [k for k in pointer.children.keys()]
        for child_value in children:
            if child_value not in list_of_values_to_remove:
                pointer.children.pop(child_value)
            else:
                self.prune(list_of_values_to_remove, pointer.children[child_value])


class Node:
    def __init__(self):
        self.value = None
        self.children = {}
        self.is_word = False

    def __repr__(self):
        return "<'{}' (node) / {}>".format(self.value, len(self.children))

    def append(self, list_of_values):
        if len(list_of_values) == 0:
            # list empty- return
            self.is_word = True
            return
        if list_of_values[0] in self.children:
            target = self.children[list_of_values[0]]
        else:
            target = Node()
            target.value = list_of_values[0]
        target.append(list_of_values[1:])
        self.children[target.value] = target

    def find_child(self, value):
        return self.children[value]

    def has_child(self, value):
        return value in self.children
