class Input:
    def __init__(self):
        self.inputStr = ''

    def set(self, s: str):
        self.inputStr = s

    def get_input(self, idx: int = None):
        if idx is None:
            return self.inputStr
        else:
            return self.inputStr[idx]

    def is_empty(self):
        if not self.inputStr:
            return True
        else:
            return False
