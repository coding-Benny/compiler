class TableDriven:
    def __init__(self):
        self.currentState = 'p'  # This means a start state.
        self.finalStates = ['r']  # This means a list of final states.
        self.table = {  # This means a state transition table.
            'p': {'0': 'q', '1': 'p'},
            'q': {'0': 'r', '1': 'p'},
            'r': {'0': 'r', '1': 'r'}
        }
        # This means a list of valid input symbols taken from the state transition table.
        self.inputSymbols = list(self.table.get(list(self.table.keys())[0]).keys())

    def progress(self, symbols):
        # Check for invalid input symbols.
        if not all(char in self.inputSymbols for char in symbols):
            return

        # State transition for input symbols
        for symbol in symbols:
            self.currentState = self.table[self.currentState][symbol]

    def is_accepted(self):
        if self.currentState in self.finalStates:
            return True
        else:
            return False


def main():
    dfa = TableDriven()
    input_string = input('input string = ')
    dfa.progress(input_string)
    if dfa.is_accepted():
        print('{} is accepted!!!'.format(input_string))
    else:
        print('{} is NOT accepted!!!'.format(input_string))
    print('programmed by JeongHyeon Lee')


if __name__ == "__main__":
    main()
