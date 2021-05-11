class Stack:
    def __init__(self):
        self.content = ['$']

    def expand(self, s: str):
        self.pop()
        for element in s[::-1]:
            self.push(element)

    def push(self, c):
        self.content.append(c)

    def pop(self):
        self.content.pop()

    def get_stack_top(self):
        return self.content[-1]

    def is_empty(self):
        if not self.content:
            return True
        else:
            return False

    def get_stack(self):
        return self.content
