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
        self.lexeme = ''
        self.finalStates = [
            STATE.S_accept_id,
            STATE.S_accept_equal,
            STATE.S_accept_decimal,
            STATE.S_accept_plus,
            STATE.S_accept_add_assign,
            STATE.S_accept_minus,
            STATE.S_accept_sub_assign,
            STATE.S_accept_func_annotation,
            STATE.S_accept_mult,
            STATE.S_accept_mult_assign,
            STATE.S_accept_exp,
            STATE.S_accept_exp_assign,
            STATE.S_accept_div,
            STATE.S_accept_div_assign,
            STATE.S_accept_floor_div,
            STATE.S_accept_floor_div_assign,
            STATE.S_accept_modulus,
            STATE.S_accept_modulus_assign,
            STATE.S_accept_less,
            STATE.S_accept_less_equal,
            STATE.S_accept_left_shift,
            STATE.S_accept_left_shift_assign,
            STATE.S_accept_greater,
            STATE.S_accept_greater_equal,
            STATE.S_accept_right_shift,
            STATE.S_accept_right_shift_assign,
            STATE.S_accept_and,
            STATE.S_accept_and_assignment,
            STATE.S_accept_or,
            STATE.S_accept_or_assignment,
            STATE.S_accept_xor,
            STATE.S_accept_xor_assignment,
            STATE.S_accept_not,
            STATE.S_accept_colon,
            STATE.S_accept_assign1,
            STATE.S_accept_assign2,
            STATE.S_accept_not_equal,
            STATE.S_accept_lparen,
            STATE.S_accept_rparen,
            STATE.S_accept_lbrace,
            STATE.S_accept_rbrace,
            STATE.S_accept_lbracket,
            STATE.S_accept_rbracket,
            STATE.S_accept_comma,
            STATE.S_accept_period,
            STATE.S_accept_semicolon,
            STATE.S_accept_string1,
            STATE.S_accept_string2
        ]
        self.table = {
            STATE.S_start: {
                SYMBOL.sb_letter: STATE.S_in_id,
                SYMBOL.sb_digit: STATE.S_accept_decimal,
                SYMBOL.sb_equal: STATE.S_in_equal,
                SYMBOL.sb_plus: STATE.S_in_plus,
                SYMBOL.sb_minus: STATE.S_in_minus,
                SYMBOL.sb_multiplication: STATE.S_in_multiplication,
                SYMBOL.sb_division: STATE.S_in_division,
                SYMBOL.sb_modulus: STATE.S_in_modulus,
                SYMBOL.sb_less: STATE.S_in_less,
                SYMBOL.sb_greater: STATE.S_in_greater,
                SYMBOL.sb_and: STATE.S_in_and,
                SYMBOL.sb_or: STATE.S_in_or,
                SYMBOL.sb_xor: STATE.S_in_xor,
                SYMBOL.sb_tilde: STATE.S_accept_not,
                SYMBOL.sb_colon: STATE.S_in_assign,
                SYMBOL.sb_exclamation: STATE.S_in_not,
                SYMBOL.sb_lparen: STATE.S_accept_lparen,
                SYMBOL.sb_rparen: STATE.S_accept_rparen,
                SYMBOL.sb_lbrace: STATE.S_accept_lbrace,
                SYMBOL.sb_rbrace: STATE.S_accept_rbrace,
                SYMBOL.sb_lbracket: STATE.S_accept_lbracket,
                SYMBOL.sb_rbracket: STATE.S_accept_rbracket,
                SYMBOL.sb_comma: STATE.S_accept_comma,
                SYMBOL.sb_period: STATE.S_accept_period,
                SYMBOL.sb_semicolon: STATE.S_accept_semicolon,
                SYMBOL.sb_single_quot: STATE.S_in_string1,
                SYMBOL.sb_double_quot: STATE.S_in_string2,
                SYMBOL.sb_hash: STATE.S_accept_comment,
                SYMBOL.sb_backslash: STATE.S_escape,
            },
            STATE.S_in_id: {
                SYMBOL.sb_letter: STATE.S_in_id,
                SYMBOL.sb_digit: STATE.S_in_id,
                SYMBOL.sb_other: STATE.S_accept_id
            },
            STATE.S_in_plus: {  # +
                SYMBOL.sb_equal: STATE.S_accept_add_assign,  # +=
                SYMBOL.sb_other: STATE.S_accept_plus  # +
            },
            STATE.S_in_minus: {  # -
                SYMBOL.sb_equal: STATE.S_accept_sub_assign,  # -=
                SYMBOL.sb_greater: STATE.S_accept_func_annotation,  # ->
                SYMBOL.sb_other: STATE.S_accept_minus  # -
            },
            STATE.S_in_multiplication: {  # *
                SYMBOL.sb_multiplication: STATE.S_in_exp,  # **
                SYMBOL.sb_equal: STATE.S_accept_mult_assign,  # *=
                SYMBOL.sb_other: STATE.S_accept_mult  # *
            },
            STATE.S_in_exp: {  # **
                SYMBOL.sb_equal: STATE.S_accept_exp_assign,  # **=
                SYMBOL.sb_other: STATE.S_accept_exp  # **
            },
            STATE.S_in_division: {  # /
                SYMBOL.sb_division: STATE.S_in_floor_div,  # //
                SYMBOL.sb_equal: STATE.S_accept_div_assign,  # /=
                SYMBOL.sb_other: STATE.S_accept_div  # /
            },
            STATE.S_in_floor_div: {  # //
                SYMBOL.sb_equal: STATE.S_accept_floor_div_assign,  # //=
                SYMBOL.sb_other: STATE.S_accept_floor_div  # //
            },
            STATE.S_in_modulus: {  # %
                SYMBOL.sb_equal: STATE.S_accept_modulus_assign,  # %=
                SYMBOL.sb_other: STATE.S_accept_modulus  # %
            },
            STATE.S_in_less: {  # <
                SYMBOL.sb_less: STATE.S_in_left_shift,  # <<
                SYMBOL.sb_equal: STATE.S_accept_less_equal,  # <=
                SYMBOL.sb_other: STATE.S_accept_less  # <
            },
            STATE.S_in_left_shift: {  # <<
                SYMBOL.sb_equal: STATE.S_accept_left_shift_assign,  # <<=
                SYMBOL.sb_other: STATE.S_accept_left_shift  # <<
            },
            STATE.S_in_greater: {  # >
                SYMBOL.sb_greater: STATE.S_in_right_shift,  # >>
                SYMBOL.sb_equal: STATE.S_accept_greater_equal,  # >=
                SYMBOL.sb_other: STATE.S_accept_greater  # >
            },
            STATE.S_in_right_shift: {  # >>
                SYMBOL.sb_equal: STATE.S_accept_right_shift_assign,  # >>=
                SYMBOL.sb_other: STATE.S_accept_right_shift  # >>
            },
            STATE.S_in_and: {  # &
                SYMBOL.sb_equal: STATE.S_accept_and_assignment,  # &=
                SYMBOL.sb_other: STATE.S_accept_and  # &
            },
            STATE.S_in_or: {  # |
                SYMBOL.sb_equal: STATE.S_accept_or_assignment,  # |=
                SYMBOL.sb_other: STATE.S_accept_or  # |
            },
            STATE.S_in_xor: {
                SYMBOL.sb_equal: STATE.S_accept_xor_assignment,  # ^=
                SYMBOL.sb_other: STATE.S_accept_xor  # ^
            },
            STATE.S_in_assign: {  # :
                SYMBOL.sb_equal: STATE.S_accept_assign1,  # :=
                SYMBOL.sb_other: STATE.S_accept_colon  # :
            },
            STATE.S_in_equal: {  # =
                SYMBOL.sb_equal: STATE.S_accept_equal,  # ==
                SYMBOL.sb_other: STATE.S_accept_assign2  # =
            },
            STATE.S_in_not: {  # !
                SYMBOL.sb_equal: STATE.S_accept_not_equal  # !=
            },
            STATE.S_in_string1: {
                SYMBOL.sb_letter: STATE.S_in_string1,
                SYMBOL.sb_digit: STATE.S_in_string1,
                SYMBOL.sb_other: STATE.S_in_string1,
                SYMBOL.sb_single_quot: STATE.S_accept_string1
            },
            STATE.S_in_string2: {
                SYMBOL.sb_letter: STATE.S_in_string2,
                SYMBOL.sb_digit: STATE.S_in_string2,
                SYMBOL.sb_other: STATE.S_in_string2,
                SYMBOL.sb_double_quot: STATE.S_accept_string2
            }
        }
        self.keywords = [
            'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise',
            'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try',
            'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with',
            'async', 'elif', 'if', 'or', 'yield'
        ]

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
    elif character == '+':
        cur_sb = SYMBOL.sb_plus
    elif character == '-':
        cur_sb = SYMBOL.sb_minus
    elif character == '*':
        cur_sb = SYMBOL.sb_multiplication
    elif character == '/':
        cur_sb = SYMBOL.sb_division
    elif character == '%':
        cur_sb = SYMBOL.sb_modulus
    elif character == '=':
        cur_sb = SYMBOL.sb_equal
    elif character == '>':
        cur_sb = SYMBOL.sb_greater
    elif character == '<':
        cur_sb = SYMBOL.sb_less
    elif character == '&':
        cur_sb = SYMBOL.sb_and
    elif character == '|':
        cur_sb = SYMBOL.sb_or
    elif character == '^':
        cur_sb = SYMBOL.sb_xor
    elif character == '~':
        cur_sb = SYMBOL.sb_tilde
    elif character == ':':
        cur_sb = SYMBOL.sb_colon
    elif character == ';':
        cur_sb = SYMBOL.sb_semicolon
    elif character == '!':
        cur_sb = SYMBOL.sb_exclamation
    elif character == '@':
        cur_sb = SYMBOL.sb_at
    elif character == '.':
        cur_sb = SYMBOL.sb_period
    elif character == ',':
        cur_sb = SYMBOL.sb_comma
    elif character == '\'':
        cur_sb = SYMBOL.sb_single_quot
    elif character == '\"':
        cur_sb = SYMBOL.sb_double_quot
    elif character == '(':
        cur_sb = SYMBOL.sb_lparen
    elif character == ')':
        cur_sb = SYMBOL.sb_rparen
    elif character == '{':
        cur_sb = SYMBOL.sb_lbrace
    elif character == '}':
        cur_sb = SYMBOL.sb_rbrace
    elif character == '[':
        cur_sb = SYMBOL.sb_lbracket
    elif character == ']':
        cur_sb = SYMBOL.sb_rbracket
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
