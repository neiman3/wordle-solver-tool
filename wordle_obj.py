class WordleDict:
    def __init__(self):
        self.head = None

    def is_empty(self):
        if self.head is None:
            return True
        return False


class Word:
    def __init__(self, value, freq_data, prev):
        self.value = value.lower()
        self.rating = 0
        self.next = None
        self.prev = prev

        for letter in self.value:
            for i in range(0, len(freq_data)):
                if freq_data[i][0] == letter:
                    self.rating += freq_data[i][1]
                    pass

    def is_first(self):
        if self.prev is None:
            return True
        return False

    def is_last(self):
        if self.next is None:
            return True
        return False

    def go_next(self):
        return self.next

    def go_prev(self):
        return self.prev
