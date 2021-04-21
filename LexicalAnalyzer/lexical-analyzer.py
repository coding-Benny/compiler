import sys
from state import *
from my_token import *
from symbol import *
import re

token = Token
symbol_list = []
my_symbol_table = SymbolTable(szSymbol=symbol_list)


class LexicalAnalyzer:
    def __init__(self):
        self.currentState = STATE.S_start
        self.finalStates = [STATE.S_accept_id, STATE.S_accept_equal, STATE.S_accept_decimal]
        self.lexeme = ''
        self.table = {
            STATE.S_start: {SYMBOL.sb_letter: STATE.S_in_id, SYMBOL.sb_digit: STATE.S_accept_decimal,
                            SYMBOL.sb_equal: STATE.S_accept_equal},
            STATE.S_in_id: {SYMBOL.sb_letter: STATE.S_in_id, SYMBOL.sb_digit: STATE.S_in_id,
                            SYMBOL.sb_other: STATE.S_accept_id},
        }
        self.keywords = ['False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise',
                         'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try',
                         'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with',
                         'async', 'elif', 'if', 'or', 'yield']

    def progress(self, symbols):
        # State transition for input symbols
        for symbol in symbols:
            if self.currentState == STATE.S_start and (symbol == ' ' or symbol == '\n'):
                continue
            current_symbol = match_symbol(symbol)
            if current_symbol != SYMBOL.sb_other:
                self.lexeme += symbol
            self.currentState = self.table[self.currentState][current_symbol]

            # Check if it is accepted
            check_acceptance(self, self.currentState)


def match_symbol(character):
    cur_sb = None
    if bool(re.match('[a-zA-Z]', character)):
        cur_sb = SYMBOL.sb_letter
    elif bool(re.match('[0-9]', character)):
        cur_sb = SYMBOL.sb_digit
    elif character == '=':
        cur_sb = SYMBOL.sb_equal
    elif bool(re.match('[^0-9a-zA-Z]', character)):
        cur_sb = SYMBOL.sb_other
    return cur_sb


def check_keyword(self, lexeme: str):
    if lexeme in self.keywords:
        print('lexeme {} is in keywords!!!'.format(lexeme))
        return self.keywords.index(lexeme)
    return None


def insert_symbol_table(lexeme: str):
    for i in range(my_symbol_table.nSymbol):
        if my_symbol_table.szSymbol[i] == lexeme:
            return i
    my_symbol_table.szSymbol.append(lexeme)
    my_symbol_table.nSymbol += 1
    return my_symbol_table.nSymbol - 1


def check_acceptance(self, state: STATE):
    if state in self.finalStates:
        if state == STATE.S_accept_id:
            # Check if it is a keyword.
            key_num = check_keyword(self, self.lexeme)
            if key_num:
                token.number = key_num
            else:
                token.number = TOKEN.Token_id
                token.value = insert_symbol_table(self.lexeme)
        else:
            token.number = TOKEN.Token_equal

        print(self.lexeme.strip(), state, token.number)
        # Initialize state
        self.currentState = STATE.S_start
        self.lexeme = ''


def main():
    # 인자로 넘긴 input file 내용 전체를 읽어들임
    with open(sys.argv[1], "r") as source_code:
        code = source_code.read()
    source_code.close()

    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.progress(code)

    # 인자로 넘긴 output file 에 쓰기
    with open(sys.argv[2], "w") as output:
        output.write('\n'.join(my_symbol_table.szSymbol))
    output.close()
    print('programmed by JeongHyeon Lee')


if __name__ == '__main__':
    main()
