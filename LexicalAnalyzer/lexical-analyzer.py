import sys
from symbol import *
from my_token import *
from literal import *

token_table = TokenTable()
value_cnt = 1


class LexicalAnalyzer:
    def __init__(self):
        self.currentState = STATE.S_start
        self.lexeme = ''
        self.finalStates = [
            STATE.S_accept_id,
            STATE.S_accept_equal,
            STATE.S_accept_zero,
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
                Symbol.sb_letter: STATE.S_in_id,
                Symbol.sb_zero: STATE.S_accept_zero,
                Symbol.sb_number: STATE.S_in_decimal,
                Symbol.sb_equal: STATE.S_in_equal,
                Symbol.sb_plus: STATE.S_in_plus,
                Symbol.sb_minus: STATE.S_in_minus,
                Symbol.sb_multiplication: STATE.S_in_multiplication,
                Symbol.sb_division: STATE.S_in_division,
                Symbol.sb_modulus: STATE.S_in_modulus,
                Symbol.sb_less: STATE.S_in_less,
                Symbol.sb_greater: STATE.S_in_greater,
                Symbol.sb_and: STATE.S_in_and,
                Symbol.sb_or: STATE.S_in_or,
                Symbol.sb_xor: STATE.S_in_xor,
                Symbol.sb_tilde: STATE.S_accept_not,
                Symbol.sb_colon: STATE.S_in_assign,
                Symbol.sb_exclamation: STATE.S_in_not,
                Symbol.sb_lparen: STATE.S_accept_lparen,
                Symbol.sb_rparen: STATE.S_accept_rparen,
                Symbol.sb_lbrace: STATE.S_accept_lbrace,
                Symbol.sb_rbrace: STATE.S_accept_rbrace,
                Symbol.sb_lbracket: STATE.S_accept_lbracket,
                Symbol.sb_rbracket: STATE.S_accept_rbracket,
                Symbol.sb_comma: STATE.S_accept_comma,
                Symbol.sb_period: STATE.S_accept_period,
                Symbol.sb_semicolon: STATE.S_accept_semicolon,
                Symbol.sb_single_quot: STATE.S_in_string1,
                Symbol.sb_double_quot: STATE.S_in_string2,
                Symbol.sb_hash: STATE.S_accept_comment,
                Symbol.sb_backslash: STATE.S_escape,
            },
            STATE.S_in_id: {
                Symbol.sb_letter: STATE.S_in_id,
                Symbol.sb_digit: STATE.S_in_id,
                Symbol.sb_other: STATE.S_accept_id
            },
            STATE.S_in_decimal: {
                Symbol.sb_digit: STATE.S_in_decimal,
                Symbol.sb_other: STATE.S_accept_decimal
            },
            STATE.S_in_plus: {  # +
                Symbol.sb_equal: STATE.S_accept_add_assign,  # +=
                Symbol.sb_other: STATE.S_accept_plus  # +
            },
            STATE.S_in_minus: {  # -
                Symbol.sb_equal: STATE.S_accept_sub_assign,  # -=
                Symbol.sb_greater: STATE.S_accept_func_annotation,  # ->
                Symbol.sb_other: STATE.S_accept_minus  # -
            },
            STATE.S_in_multiplication: {  # *
                Symbol.sb_multiplication: STATE.S_in_exp,  # **
                Symbol.sb_equal: STATE.S_accept_mult_assign,  # *=
                Symbol.sb_other: STATE.S_accept_mult  # *
            },
            STATE.S_in_exp: {  # **
                Symbol.sb_equal: STATE.S_accept_exp_assign,  # **=
                Symbol.sb_other: STATE.S_accept_exp  # **
            },
            STATE.S_in_division: {  # /
                Symbol.sb_division: STATE.S_in_floor_div,  # //
                Symbol.sb_equal: STATE.S_accept_div_assign,  # /=
                Symbol.sb_other: STATE.S_accept_div  # /
            },
            STATE.S_in_floor_div: {  # //
                Symbol.sb_equal: STATE.S_accept_floor_div_assign,  # //=
                Symbol.sb_other: STATE.S_accept_floor_div  # //
            },
            STATE.S_in_modulus: {  # %
                Symbol.sb_equal: STATE.S_accept_modulus_assign,  # %=
                Symbol.sb_other: STATE.S_accept_modulus  # %
            },
            STATE.S_in_less: {  # <
                Symbol.sb_less: STATE.S_in_left_shift,  # <<
                Symbol.sb_equal: STATE.S_accept_less_equal,  # <=
                Symbol.sb_other: STATE.S_accept_less  # <
            },
            STATE.S_in_left_shift: {  # <<
                Symbol.sb_equal: STATE.S_accept_left_shift_assign,  # <<=
                Symbol.sb_other: STATE.S_accept_left_shift  # <<
            },
            STATE.S_in_greater: {  # >
                Symbol.sb_greater: STATE.S_in_right_shift,  # >>
                Symbol.sb_equal: STATE.S_accept_greater_equal,  # >=
                Symbol.sb_other: STATE.S_accept_greater  # >
            },
            STATE.S_in_right_shift: {  # >>
                Symbol.sb_equal: STATE.S_accept_right_shift_assign,  # >>=
                Symbol.sb_other: STATE.S_accept_right_shift  # >>
            },
            STATE.S_in_and: {  # &
                Symbol.sb_equal: STATE.S_accept_and_assignment,  # &=
                Symbol.sb_other: STATE.S_accept_and  # &
            },
            STATE.S_in_or: {  # |
                Symbol.sb_equal: STATE.S_accept_or_assignment,  # |=
                Symbol.sb_other: STATE.S_accept_or  # |
            },
            STATE.S_in_xor: {
                Symbol.sb_equal: STATE.S_accept_xor_assignment,  # ^=
                Symbol.sb_other: STATE.S_accept_xor  # ^
            },
            STATE.S_in_assign: {  # :
                Symbol.sb_equal: STATE.S_accept_assign1,  # :=
                Symbol.sb_other: STATE.S_accept_colon  # :
            },
            STATE.S_in_equal: {  # =
                Symbol.sb_equal: STATE.S_accept_equal,  # ==
                Symbol.sb_other: STATE.S_accept_assign2  # =
            },
            STATE.S_in_not: {  # !
                Symbol.sb_equal: STATE.S_accept_not_equal  # !=
            },
            STATE.S_in_string1: {
                Symbol.sb_letter: STATE.S_in_string1,
                Symbol.sb_other: STATE.S_in_string1,
                Symbol.sb_single_quot: STATE.S_accept_string1
            },
            STATE.S_in_string2: {
                Symbol.sb_letter: STATE.S_in_string2,
                Symbol.sb_other: STATE.S_in_string2,
                Symbol.sb_double_quot: STATE.S_accept_string2
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
            current_symbol = identify_symbol(symbol, self.currentState)
            if current_symbol != Symbol.sb_other:
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
        token = Token()
        if state == STATE.S_accept_id:
            global value_cnt
            # Check if it is a keyword.
            key_num = check_keyword(self, self.lexeme)
            if key_num:
                token.set_token(key_num)
            else:
                token.set_token(TOKEN.Token_id)
                token.set_token_value(value_cnt)
                insert_symbol_table(self.lexeme)
                value_cnt += 1
        elif state == STATE.S_accept_equal:
            token.set_token(TOKEN.Token_equal)
        elif state == STATE.S_accept_zero:
            token.set_token(TOKEN.Token_zero)
            insert_literal_table(self.lexeme)
        elif state == STATE.S_accept_decimal:
            token.set_token(TOKEN.Token_decimal)
            insert_literal_table(self.lexeme)
        elif state == STATE.S_accept_plus:
            token.set_token(TOKEN.Token_plus)
        elif state == STATE.S_accept_add_assign:
            token.set_token(TOKEN.Token_add_assign)
        elif state == STATE.S_accept_minus:
            token.set_token(TOKEN.Token_minus)
        elif state == STATE.S_accept_sub_assign:
            token.set_token(TOKEN.Token_sub_assign)
        elif state == STATE.S_accept_func_annotation:
            token.set_token(TOKEN.Token_func_annotation)
        elif state == STATE.S_accept_mult:
            token.set_token(TOKEN.Token_mult)
        elif state == STATE.S_accept_mult_assign:
            token.set_token(TOKEN.Token_mult_assign)
        elif state == STATE.S_accept_exp:
            token.set_token(TOKEN.Token_exp)
        elif state == STATE.S_accept_exp_assign:
            token.set_token(TOKEN.Token_exp_assign)
        elif state == STATE.S_accept_div:
            token.set_token(TOKEN.Token_div)
        elif state == STATE.S_accept_div_assign:
            token.set_token(TOKEN.Token_div_assign)
        elif state == STATE.S_accept_floor_div:
            token.set_token(TOKEN.Token_floor_div)
        elif state == STATE.S_accept_floor_div_assign:
            token.set_token(TOKEN.Token_floor_div_assign)
        elif state == STATE.S_accept_modulus:
            token.set_token(TOKEN.Token_modulus)
        elif state == STATE.S_accept_modulus_assign:
            token.set_token(TOKEN.Token_modulus_assign)
        elif state == STATE.S_accept_less:
            token.set_token(TOKEN.Token_less)
        elif state == STATE.S_accept_less_equal:
            token.set_token(TOKEN.Token_less_equal)
        elif state == STATE.S_accept_left_shift:
            token.set_token(TOKEN.Token_left_shift)
        elif state == STATE.S_accept_left_shift_assign:
            token.set_token(TOKEN.Token_left_shift_assign)
        elif state == STATE.S_accept_greater:
            token.set_token(TOKEN.Token_greater)
        elif state == STATE.S_accept_greater_equal:
            token.set_token(TOKEN.Token_greater_equal)
        elif state == STATE.S_accept_right_shift:
            token.set_token(TOKEN.Token_right_shift)
        elif state == STATE.S_accept_right_shift_assign:
            token.set_token(TOKEN.Token_right_shift_assign)
        elif state == STATE.S_accept_and:
            token.set_token(TOKEN.Token_and)
        elif state == STATE.S_accept_and_assignment:
            token.set_token(TOKEN.Token_and_assign)
        elif state == STATE.S_accept_or:
            token.set_token(TOKEN.Token_or)
        elif state == STATE.S_accept_or_assignment:
            token.set_token(TOKEN.Token_or_assign)
        elif state == STATE.S_accept_xor:
            token.set_token(TOKEN.Token_xor)
        elif state == STATE.S_accept_xor_assignment:
            token.set_token(TOKEN.Token_xor_assign)
        elif state == STATE.S_accept_not:
            token.set_token(TOKEN.Token_not)
        elif state == STATE.S_accept_colon:
            token.set_token(TOKEN.Token_colon)
        elif state == STATE.S_accept_assign1:
            token.set_token(TOKEN.Token_assign1)
        elif state == STATE.S_accept_assign2:
            token.set_token(TOKEN.Token_assign2)
        elif state == STATE.S_accept_not_equal:
            token.set_token(TOKEN.Token_not_equal)
        elif state == STATE.S_accept_lparen:
            token.set_token(TOKEN.Token_left_paren)
        elif state == STATE.S_accept_rparen:
            token.set_token(TOKEN.Token_right_paren)
        elif state == STATE.S_accept_lbrace:
            token.set_token(TOKEN.Token_left_brace)
        elif state == STATE.S_accept_rbrace:
            token.set_token(TOKEN.Token_right_brace)
        elif state == STATE.S_accept_lbracket:
            token.set_token(TOKEN.Token_left_bracket)
        elif state == STATE.S_accept_rbracket:
            token.set_token(TOKEN.Token_right_bracket)
        elif state == STATE.S_accept_comma:
            token.set_token(TOKEN.Token_comma)
        elif state == STATE.S_accept_period:
            token.set_token(TOKEN.Token_period)
        elif state == STATE.S_accept_semicolon:
            token.set_token(TOKEN.Token_semicolon)
        elif state == STATE.S_accept_string1:
            token.set_token(TOKEN.Token_string1)
            insert_literal_table(self.lexeme)
        elif state == STATE.S_accept_string2:
            token.set_token(TOKEN.Token_string2)
            insert_literal_table(self.lexeme)

        token_table.add_token(token)
        print(self.lexeme, state, token.get_token())
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
        output.write("==========================[ Token Table ]==========================\n")
        output.write(token_table.get_all_tokens())
        output.write("==========================[ Symbol Table ]=========================\n")
        output.write(symbol_table.get_all_symbols())
        output.write("=========================[ Literal Table ]=========================\n")
        output.write(literal_table.get_all_literals())
    output.close()
    print('programmed by JeongHyeon Lee')


if __name__ == '__main__':
    main()
