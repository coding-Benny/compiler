class Stack:
    def __init__(self):
        self.__content = []

    def push(self, c: str):
        self.__content.append(c)

    def pop(self):
        self.__content.pop()

    def get_stack_top(self):
        return self.__content[-1]

    def get_stack(self):
        return self.__content

    def get_element(self, n: int):
        return self.__content[n]
