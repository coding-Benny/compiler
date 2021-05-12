class Stack:
    def __init__(self):
        self.__content = ['$']

    def expand(self, s: str):
        self.pop()
        for element in s[::-1]:
            self.push(element)

    def push(self, c):
        self.__content.append(c)

    def pop(self):
        self.__content.pop()

    def get_stack_top(self):
        return self.__content[-1]

    def is_empty(self):
        if self.__content[0] == '$' and len(self.__content) == 1:
            return True
        else:
            return False

    def get_stack(self):
        return self.__content
