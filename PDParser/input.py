class Input:
    def __init__(self):
        self.__inputStr = ''

    def set(self, s: str):
        self.__inputStr = s

    def get_input(self, idx: int = None):
        if idx is None:
            return self.__inputStr
        else:
            return self.__inputStr[idx]

    def is_empty(self):
        if self.__inputStr[0] == '$' and len(self.__inputStr) == 1:
            return True
        else:
            return False

    def increment(self):
        return self.__inputStr[1:]
