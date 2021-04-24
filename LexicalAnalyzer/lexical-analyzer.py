import sys
from symbol import *
from my_token import *
from literal import *

token_table = TokenTable()
is_error_occurred = False
error_msg = ''


class LexicalAnalyzer:
    def __init__(self):
        self.currentState = State.START
        self.lexeme = ''
        self.finalStates = [
            State.ACCEPT_ID,
            State.ACCEPT_EQUAL,
            State.ACCEPT_ZERO,
            State.ACCEPT_DECIMAL,
            State.ACCEPT_PLUS,
            State.ACCEPT_ADD_ASSIGNMENT,
            State.ACCEPT_MINUS,
            State.ACCEPT_SUB_ASSIGNMENT,
            State.ACCEPT_FUNC_ANNOTATION,
            State.ACCEPT_MULTIPLICATION,
            State.ACCEPT_MULTIPLICATION_ASSIGNMENT,
            State.ACCEPT_EXP,
            State.ACCEPT_EXP_ASSIGNMENT,
            State.ACCEPT_DIVISION,
            State.ACCEPT_DIVISION_ASSIGNMENT,
            State.ACCEPT_FLOOR_DIV,
            State.ACCEPT_FLOOR_DIV_ASSIGNMENT,
            State.ACCEPT_MODULUS,
            State.ACCEPT_MODULUS_ASSIGNMENT,
            State.ACCEPT_LESS,
            State.ACCEPT_LESS_EQUAL,
            State.ACCEPT_LSHIFT,
            State.ACCEPT_LSHIFT_ASSIGNMENT,
            State.ACCEPT_GREATER,
            State.ACCEPT_GREATER_EQUAL,
            State.ACCEPT_RSHIFT,
            State.ACCEPT_RSHIFT_ASSIGNMENT,
            State.ACCEPT_AND,
            State.ACCEPT_AND_ASSIGNMENT,
            State.ACCEPT_OR,
            State.ACCEPT_OR_ASSIGNMENT,
            State.ACCEPT_XOR,
            State.ACCEPT_XOR_ASSIGNMENT,
            State.ACCEPT_NOT,
            State.ACCEPT_COLON,
            State.ACCEPT_ASSIGNMENT1,
            State.ACCEPT_ASSIGNMENT2,
            State.ACCEPT_NOT_EQUAL,
            State.ACCEPT_LPAREN,
            State.ACCEPT_RPAREN,
            State.ACCEPT_LBRACE,
            State.ACCEPT_RBRACE,
            State.ACCEPT_LBRACKET,
            State.ACCEPT_RBRACKET,
            State.S_accept_comma,
            State.ACCEPT_PERIOD,
            State.ACCEPT_SEMICOLON,
            State.ACCEPT_STRING1,
            State.ACCEPT_STRING2,
            State.ACCEPT_SPACE,
            State.ACCEPT_NEWLINE,
        ]
        self.table = {
            State.START: {
                Symbol.LETTER: State.IN_ID,
                Symbol.ZERO: State.ACCEPT_ZERO,
                Symbol.NUMBER: State.IN_DECIMAL,
                Symbol.EQUAL: State.IN_EQUAL,
                Symbol.PLUS: State.IN_PLUS,
                Symbol.MINUS: State.IN_MINUS,
                Symbol.ASTERISK: State.IN_MULTIPLICATION,
                Symbol.DIVISION: State.IN_DIVISION,
                Symbol.MODULUS: State.IN_MODULUS,
                Symbol.LESS: State.IN_LESS,
                Symbol.GREATER: State.IN_GREATER,
                Symbol.AMPERSAND: State.IN_AND,
                Symbol.PIPE: State.IN_OR,
                Symbol.CARET: State.IN_XOR,
                Symbol.TILDE: State.ACCEPT_NOT,
                Symbol.COLON: State.IN_ASSIGNMENT,
                Symbol.BANG: State.IN_NOT,
                Symbol.LPAREN: State.ACCEPT_LPAREN,
                Symbol.RPAREN: State.ACCEPT_RPAREN,
                Symbol.LBRACE: State.ACCEPT_LBRACE,
                Symbol.RBRACE: State.ACCEPT_RBRACE,
                Symbol.LBRACKET: State.ACCEPT_LBRACKET,
                Symbol.RBRACKET: State.ACCEPT_RBRACKET,
                Symbol.COMMA: State.S_accept_comma,
                Symbol.PERIOD: State.ACCEPT_PERIOD,
                Symbol.SEMICOLON: State.ACCEPT_SEMICOLON,
                Symbol.SINGLE_QUOT: State.IN_STRING1,
                Symbol.DOUBLE_QUOT: State.IN_STRING2,
                Symbol.HASH: State.ACCEPT_COMMENT,
                Symbol.BACKSLASH: State.ESCAPE,
                Symbol.SPACE: State.ACCEPT_SPACE,
                Symbol.NEWLINE: State.ACCEPT_NEWLINE,
            },
            State.IN_ID: {
                Symbol.LETTER: State.IN_ID,
                Symbol.DIGIT: State.IN_ID,
                Symbol.OTHER: State.ACCEPT_ID
            },
            State.IN_DECIMAL: {
                Symbol.DIGIT: State.IN_DECIMAL,
                Symbol.OTHER: State.ACCEPT_DECIMAL
            },
            State.IN_PLUS: {  # +
                Symbol.EQUAL: State.ACCEPT_ADD_ASSIGNMENT,  # +=
                Symbol.OTHER: State.ACCEPT_PLUS  # +
            },
            State.IN_MINUS: {  # -
                Symbol.EQUAL: State.ACCEPT_SUB_ASSIGNMENT,  # -=
                Symbol.GREATER: State.ACCEPT_FUNC_ANNOTATION,  # ->
                Symbol.OTHER: State.ACCEPT_MINUS  # -
            },
            State.IN_MULTIPLICATION: {  # *
                Symbol.ASTERISK: State.IN_EXP,  # **
                Symbol.EQUAL: State.ACCEPT_MULTIPLICATION_ASSIGNMENT,  # *=
                Symbol.OTHER: State.ACCEPT_MULTIPLICATION  # *
            },
            State.IN_EXP: {  # **
                Symbol.EQUAL: State.ACCEPT_EXP_ASSIGNMENT,  # **=
                Symbol.OTHER: State.ACCEPT_EXP  # **
            },
            State.IN_DIVISION: {  # /
                Symbol.DIVISION: State.IN_FLOOR_DIV,  # //
                Symbol.EQUAL: State.ACCEPT_DIVISION_ASSIGNMENT,  # /=
                Symbol.OTHER: State.ACCEPT_DIVISION  # /
            },
            State.IN_FLOOR_DIV: {  # //
                Symbol.EQUAL: State.ACCEPT_FLOOR_DIV_ASSIGNMENT,  # //=
                Symbol.OTHER: State.ACCEPT_FLOOR_DIV  # //
            },
            State.IN_MODULUS: {  # %
                Symbol.EQUAL: State.ACCEPT_MODULUS_ASSIGNMENT,  # %=
                Symbol.OTHER: State.ACCEPT_MODULUS  # %
            },
            State.IN_LESS: {  # <
                Symbol.LESS: State.IN_LSHIFT,  # <<
                Symbol.EQUAL: State.ACCEPT_LESS_EQUAL,  # <=
                Symbol.OTHER: State.ACCEPT_LESS  # <
            },
            State.IN_LSHIFT: {  # <<
                Symbol.EQUAL: State.ACCEPT_LSHIFT_ASSIGNMENT,  # <<=
                Symbol.OTHER: State.ACCEPT_LSHIFT  # <<
            },
            State.IN_GREATER: {  # >
                Symbol.GREATER: State.IN_RSHIFT,  # >>
                Symbol.EQUAL: State.ACCEPT_GREATER_EQUAL,  # >=
                Symbol.OTHER: State.ACCEPT_GREATER  # >
            },
            State.IN_RSHIFT: {  # >>
                Symbol.EQUAL: State.ACCEPT_RSHIFT_ASSIGNMENT,  # >>=
                Symbol.OTHER: State.ACCEPT_RSHIFT  # >>
            },
            State.IN_AND: {  # &
                Symbol.EQUAL: State.ACCEPT_AND_ASSIGNMENT,  # &=
                Symbol.OTHER: State.ACCEPT_AND  # &
            },
            State.IN_OR: {  # |
                Symbol.EQUAL: State.ACCEPT_OR_ASSIGNMENT,  # |=
                Symbol.OTHER: State.ACCEPT_OR  # |
            },
            State.IN_XOR: {
                Symbol.EQUAL: State.ACCEPT_XOR_ASSIGNMENT,  # ^=
                Symbol.OTHER: State.ACCEPT_XOR  # ^
            },
            State.IN_ASSIGNMENT: {  # :
                Symbol.EQUAL: State.ACCEPT_ASSIGNMENT1,  # :=
                Symbol.OTHER: State.ACCEPT_COLON  # :
            },
            State.IN_EQUAL: {  # =
                Symbol.EQUAL: State.ACCEPT_EQUAL,  # ==
                Symbol.OTHER: State.ACCEPT_ASSIGNMENT2  # =
            },
            State.IN_NOT: {  # !
                Symbol.EQUAL: State.ACCEPT_NOT_EQUAL  # !=
            },
            State.IN_STRING1: {
                Symbol.LETTER: State.IN_STRING1,
                Symbol.OTHER: State.IN_STRING1,
                Symbol.SINGLE_QUOT: State.ACCEPT_STRING1
            },
            State.IN_STRING2: {
                Symbol.LETTER: State.IN_STRING2,
                Symbol.OTHER: State.IN_STRING2,
                Symbol.DOUBLE_QUOT: State.ACCEPT_STRING2
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
            if self.currentState == State.START and symbol.isspace():
                continue
            current_symbol = identify_symbol(symbol, self.currentState)
            if current_symbol is None:
                global is_error_occurred, error_msg
                is_error_occurred = True
                error_msg = "Error occurred because of the symbol {}".format(symbol)
                print(error_msg)
                break
            if current_symbol != Symbol.OTHER:
                self.lexeme += symbol
            self.currentState = self.table[self.currentState][current_symbol]

            # Check if it is accepted
            check_acceptance(self, self.currentState)

            if current_symbol == Symbol.OTHER:
                current_symbol = identify_symbol(symbol, self.currentState)
                self.lexeme += symbol
                self.currentState = self.table[self.currentState][current_symbol]
                check_acceptance(self, self.currentState)


def check_keyword(self, lexeme: str):
    if lexeme in self.keywords:
        return self.keywords.index(lexeme)
    return None


def check_acceptance(self, state: State):
    if state in self.finalStates:
        token = MyToken()
        if state == State.ACCEPT_ID:
            # Check if it is a keyword.
            key_num = check_keyword(self, self.lexeme)
            if key_num:
                token.set_token(key_num)
            else:
                token.set_token(Token.ID)
                value = insert_symbol_table(self.lexeme)
                token.set_token_value(value)
        elif state == State.ACCEPT_EQUAL:
            token.set_token(Token.EQUAL)
        elif state == State.ACCEPT_ZERO:
            token.set_token(Token.ZERO)
            insert_literal_table(self.lexeme)
        elif state == State.ACCEPT_DECIMAL:
            token.set_token(Token.DECIMAL)
            insert_literal_table(self.lexeme)
        elif state == State.ACCEPT_PLUS:
            token.set_token(Token.PLUS)
        elif state == State.ACCEPT_ADD_ASSIGNMENT:
            token.set_token(Token.ADD_ASSIGNMENT)
        elif state == State.ACCEPT_MINUS:
            token.set_token(Token.MINUS)
        elif state == State.ACCEPT_SUB_ASSIGNMENT:
            token.set_token(Token.SUB_ASSIGNMENT)
        elif state == State.ACCEPT_FUNC_ANNOTATION:
            token.set_token(Token.FUNC_ANNOTATION)
        elif state == State.ACCEPT_MULTIPLICATION:
            token.set_token(Token.MULTIPLICATION)
        elif state == State.ACCEPT_MULTIPLICATION_ASSIGNMENT:
            token.set_token(Token.MULTIPLICATION_ASSIGNMENT)
        elif state == State.ACCEPT_EXP:
            token.set_token(Token.EXP)
        elif state == State.ACCEPT_EXP_ASSIGNMENT:
            token.set_token(Token.EXP_ASSIGNMENT)
        elif state == State.ACCEPT_DIVISION:
            token.set_token(Token.DIVISION)
        elif state == State.ACCEPT_DIVISION_ASSIGNMENT:
            token.set_token(Token.DIV_ASSIGNMENT)
        elif state == State.ACCEPT_FLOOR_DIV:
            token.set_token(Token.FLOOR_DIVISION)
        elif state == State.ACCEPT_FLOOR_DIV_ASSIGNMENT:
            token.set_token(Token.FLOOR_DIV_ASSIGNMENT)
        elif state == State.ACCEPT_MODULUS:
            token.set_token(Token.MODULUS)
        elif state == State.ACCEPT_MODULUS_ASSIGNMENT:
            token.set_token(Token.MODULUS_ASSIGNMENT)
        elif state == State.ACCEPT_LESS:
            token.set_token(Token.LESS)
        elif state == State.ACCEPT_LESS_EQUAL:
            token.set_token(Token.LESS_EQUAL)
        elif state == State.ACCEPT_LSHIFT:
            token.set_token(Token.LSHIFT)
        elif state == State.ACCEPT_LSHIFT_ASSIGNMENT:
            token.set_token(Token.LSHIFT_ASSIGNMENT)
        elif state == State.ACCEPT_GREATER:
            token.set_token(Token.GREATER)
        elif state == State.ACCEPT_GREATER_EQUAL:
            token.set_token(Token.GREATER_EQUAL)
        elif state == State.ACCEPT_RSHIFT:
            token.set_token(Token.RSHIFT)
        elif state == State.ACCEPT_RSHIFT_ASSIGNMENT:
            token.set_token(Token.RSHIFT_ASSIGNMENT)
        elif state == State.ACCEPT_AND:
            token.set_token(Token.AND)
        elif state == State.ACCEPT_AND_ASSIGNMENT:
            token.set_token(Token.AND_ASSIGNMENT)
        elif state == State.ACCEPT_OR:
            token.set_token(Token.OR)
        elif state == State.ACCEPT_OR_ASSIGNMENT:
            token.set_token(Token.OR_ASSIGNMENT)
        elif state == State.ACCEPT_XOR:
            token.set_token(Token.XOR)
        elif state == State.ACCEPT_XOR_ASSIGNMENT:
            token.set_token(Token.XOR_ASSIGNMENT)
        elif state == State.ACCEPT_NOT:
            token.set_token(Token.NOT)
        elif state == State.ACCEPT_COLON:
            token.set_token(Token.COLON)
        elif state == State.ACCEPT_ASSIGNMENT1:
            token.set_token(Token.ASSIGNMENT1)
        elif state == State.ACCEPT_ASSIGNMENT2:
            token.set_token(Token.ASSIGNMENT2)
        elif state == State.ACCEPT_NOT_EQUAL:
            token.set_token(Token.NOT_EQUAL)
        elif state == State.ACCEPT_LPAREN:
            token.set_token(Token.LPAREN)
        elif state == State.ACCEPT_RPAREN:
            token.set_token(Token.RPAREN)
        elif state == State.ACCEPT_LBRACE:
            token.set_token(Token.LBRACE)
        elif state == State.ACCEPT_RBRACE:
            token.set_token(Token.RBRACE)
        elif state == State.ACCEPT_LBRACKET:
            token.set_token(Token.LBRACKET)
        elif state == State.ACCEPT_RBRACKET:
            token.set_token(Token.RBRACKET)
        elif state == State.S_accept_comma:
            token.set_token(Token.COMMA)
        elif state == State.ACCEPT_PERIOD:
            token.set_token(Token.PERIOD)
        elif state == State.ACCEPT_SEMICOLON:
            token.set_token(Token.SEMICOLON)
        elif state == State.ACCEPT_STRING1:
            token.set_token(Token.STRING1)
            insert_literal_table(self.lexeme)
        elif state == State.ACCEPT_STRING2:
            token.set_token(Token.STRING2)
            insert_literal_table(self.lexeme)
        elif state == State.ACCEPT_SPACE:
            token.set_token(Token.SPACE)
        elif state == State.ACCEPT_NEWLINE:
            token.set_token(Token.NEWLINE)

        token_table.add_token(token)
        print(self.lexeme.strip(), state, token.get_token())
        # Initialize state
        self.currentState = State.START
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
        if is_error_occurred:
            output.write(error_msg)
        else:
            output.write("==========================[ Token Table ]==========================\n")
            output.write(token_table.get_all_tokens())
            output.write("\n==========================[ Symbol Table ]=========================\n")
            output.write(symbol_table.get_all_symbols())
            output.write("\n=========================[ Literal Table ]=========================\n")
            output.write(literal_table.get_all_literals())
    output.close()
    print('programmed by JeongHyeon Lee')


if __name__ == '__main__':
    main()
