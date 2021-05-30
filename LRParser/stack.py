class Stack:
    def __init__(self):
        self.__content = []

    def expand(self, s: str):
        self.pop()
        for element in s[::-1]:
            self.push(element)

    def push(self, c: str):
        self.__content.append(c)

    def pop(self):
        self.__content.pop()

    def get_stack_top(self):
        return self.__content[-1]

    def is_empty(self):
        if not self.__content:
            return True
        else:
            return False

    def get_stack(self):
        return self.__content

    def get_element(self, n: int):
        return self.__content[n]
