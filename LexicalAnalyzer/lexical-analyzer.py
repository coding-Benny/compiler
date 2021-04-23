import sys
from symbol import *
from my_token import *


token = Token


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
            if self.currentState == STATE.S_start and symbol.isspace():
                continue
            current_symbol = match_symbol(symbol, self.currentState)
            if current_symbol != SYMBOL.sb_other:
                self.lexeme += symbol
            self.currentState = self.table[self.currentState][current_symbol]

            # Check if it is accepted
            check_acceptance(self, self.currentState)


def check_keyword(self, lexeme: str):
    if lexeme in self.keywords:
        print('lexeme {} is in keywords!!!'.format(lexeme))
        return self.keywords.index(lexeme)
    return None


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
        elif state == STATE.S_accept_equal:
            token.number = TOKEN.Token_equal
        elif state == STATE.S_accept_decimal:
            token.number = TOKEN.Token_decimal
        elif state == STATE.S_accept_plus:
            token.number = TOKEN.Token_plus
        elif state == STATE.S_accept_add_assign:
            token.number = TOKEN.Token_add_assign
        elif state == STATE.S_accept_minus:
            token.number = TOKEN.Token_minus
        elif state == STATE.S_accept_sub_assign:
            token.number = TOKEN.Token_sub_assign
        elif state == STATE.S_accept_func_annotation:
            token.number = TOKEN.Token_func_annotation
        elif state == STATE.S_accept_mult:
            token.number = TOKEN.Token_mult
        elif state == STATE.S_accept_mult_assign:
            token.number = TOKEN.Token_mult_assign
        elif state == STATE.S_accept_exp:
            token.number = TOKEN.Token_exp
        elif state == STATE.S_accept_exp_assign:
            token.number = TOKEN.Token_exp_assign
        elif state == STATE.S_accept_div:
            token.number = TOKEN.Token_div
        elif state == STATE.S_accept_div_assign:
            token.number = TOKEN.Token_div_assign
        elif state == STATE.S_accept_floor_div:
            token.number = TOKEN.Token_floor_div
        elif state == STATE.S_accept_floor_div_assign:
            token.number = TOKEN.Token_floor_div_assign
        elif state == STATE.S_accept_modulus:
            token.number = TOKEN.Token_modulus
        elif state == STATE.S_accept_modulus_assign:
            token.number = TOKEN.Token_modulus_assign
        elif state == STATE.S_accept_less:
            token.number = TOKEN.Token_less
        elif state == STATE.S_accept_less_equal:
            token.number = TOKEN.Token_less_equal
        elif state == STATE.S_accept_left_shift:
            token.number = TOKEN.Token_left_shift
        elif state == STATE.S_accept_left_shift_assign:
            token.number = TOKEN.Token_left_shift_assign
        elif state == STATE.S_accept_greater:
            token.number = TOKEN.Token_greater
        elif state == STATE.S_accept_greater_equal:
            token.number = TOKEN.Token_greater_equal
        elif state == STATE.S_accept_right_shift:
            token.number = TOKEN.Token_right_shift
        elif state == STATE.S_accept_right_shift_assign:
            token.number = TOKEN.Token_right_shift_assign
        elif state == STATE.S_accept_and:
            token.number = TOKEN.Token_and
        elif state == STATE.S_accept_and_assignment:
            token.number = TOKEN.Token_and_assign
        elif state == STATE.S_accept_or:
            token.number = TOKEN.Token_or
        elif state == STATE.S_accept_or_assignment:
            token.number = TOKEN.Token_or_assign
        elif state == STATE.S_accept_xor:
            token.number = TOKEN.Token_xor
        elif state == STATE.S_accept_xor_assignment:
            token.number = TOKEN.Token_xor_assign
        elif state == STATE.S_accept_not:
            token.number = TOKEN.Token_not
        elif state == STATE.S_accept_colon:
            token.number = TOKEN.Token_colon
        elif state == STATE.S_accept_assign1:
            token.number = TOKEN.Token_assign1
        elif state == STATE.S_accept_assign2:
            token.number = TOKEN.Token_assign2
        elif state == STATE.S_accept_not_equal:
            token.number = TOKEN.Token_not_equal
        elif state == STATE.S_accept_lparen:
            token.number = TOKEN.Token_left_paren
        elif state == STATE.S_accept_rparen:
            token.number = TOKEN.Token_right_paren
        elif state == STATE.S_accept_lbrace:
            token.number = TOKEN.Token_left_brace
        elif state == STATE.S_accept_rbrace:
            token.number = TOKEN.Token_right_brace
        elif state == STATE.S_accept_lbracket:
            token.number = TOKEN.Token_left_bracket
        elif state == STATE.S_accept_rbracket:
            token.number = TOKEN.Token_right_bracket
        elif state == STATE.S_accept_comma:
            token.number = TOKEN.Token_comma
        elif state == STATE.S_accept_period:
            token.number = TOKEN.Token_period
        elif state == STATE.S_accept_semicolon:
            token.number = TOKEN.Token_semicolon
        elif state == STATE.S_accept_string1:
            token.number = TOKEN.Token_string1
        elif state == STATE.S_accept_string2:
            token.number = TOKEN.Token_string2

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
