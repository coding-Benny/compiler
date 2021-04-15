from state import *
from my_token import *
from symbol import *
import re


class LexicalAnalyzer:
    def __init__(self):
        self.currentState = State.S_start
        self.finalStates = [State.S_accept_id]
        self.table = {
            State.S_start: {Symbol.sb_letter: State.S_in_id},
            State.S_in_id: {Symbol.sb_letter: State.S_in_id, Symbol.sb_digit: State.S_in_id,
                            Symbol.sb_other: State.S_accept_id},
        }
        self.currentSymbol = None
        self.currentToken = ''

    def progress(self, symbols):
        # Check if it is a keyword.

        # State transition for input symbols
        for symbol in symbols:
            current_symbol = match_symbol(symbol)
            self.currentState = self.table[self.currentState][current_symbol]
            print('symbol: {}'.format(current_symbol))
            print('state: {}'.format(self.currentState))

    def is_accepted(self):
        if self.currentState in self.finalStates:
            return True
        else:
            return False


def match_symbol(character):
    if bool(re.match('[a-zA-Z]', character)):
        current_symbol = Symbol.sb_letter
    elif bool(re.match('[0-9]', character)):
        current_symbol = Symbol.sb_digit
    else:
        current_symbol = Symbol.sb_other
    return current_symbol


def main():
    lexical_analyzer = LexicalAnalyzer()
    input_string = input('input string = ')
    print(input_string)
    lexical_analyzer.progress(input_string)
    if lexical_analyzer.is_accepted():
        print('{} is accepted!!!'.format(input_string))
    else:
        print('{} is NOT accepted!!!'.format(input_string))
    print('programmed by JeongHyeon Lee')


if __name__ == '__main__':
    main()
