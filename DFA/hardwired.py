class HardWired:
    def __init__(self):
        self.currentState = 'p'
        self.finalState = 'r'
        self.inputSymbols = ['0', '1']  # List of valid input symbols

    def progress(self, symbols):
        # Check for invalid input symbols.
        if not all(char in self.inputSymbols for char in symbols):
            return

        # State transition for input symbols
        for symbol in symbols:
            if self.currentState == 'p':
                if symbol == '0':
                    self.currentState = 'q'
            elif self.currentState == 'q':
                if symbol == '0':
                    self.currentState = 'r'
                elif symbol == '1':
                    self.currentState = 'p'

    def is_accepted(self):
        if self.currentState in self.finalState:
            return True
        else:
            return False


def main():
    dfa = HardWired()
    input_string = input('input string = ')
    dfa.progress(input_string)
    if dfa.is_accepted():
        print('{} is accepted!!!'.format(input_string))
    else:
        print('{} is NOT accepted!!!'.format(input_string))
    print('programmed by JeongHyeon Lee')


if __name__ == "__main__":
    main()
