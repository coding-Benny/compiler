class Input:
    def __init__(self):
        self.__string = ''

    def set(self, s: str):
        self.__string = s

    def get_input(self, idx: int = None):
        if idx is None:
            return self.__string
        else:
            return self.__string[idx]

    def is_empty(self):
        if not self.__string:
            return True
        else:
            return False

    def increment(self):
        return self.__string[1:]
