import sys
from symbol import *
from my_token import *
from literal import *

token_table = TokenTable()
error_occurred = False
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
            State.ACCEPT_OCTAL,
            State.ACCEPT_HEX,
            State.ACCEPT_PLUS,
            State.ACCEPT_ADD_ASSIGN,
            State.ACCEPT_MINUS,
            State.ACCEPT_SUB_ASSIGN,
            State.ACCEPT_FUNC_ANNOTATION,
            State.ACCEPT_MULTIPLICATION,
            State.ACCEPT_MULTIPLICATION_ASSIGN,
            State.ACCEPT_EXP,
            State.ACCEPT_EXP_ASSIGN,
            State.ACCEPT_DIVISION,
            State.ACCEPT_DIVISION_ASSIGN,
            State.ACCEPT_FLOOR_DIV,
            State.ACCEPT_FLOOR_DIV_ASSIGN,
            State.ACCEPT_MODULUS,
            State.ACCEPT_MODULUS_ASSIGN,
            State.ACCEPT_LESS,
            State.ACCEPT_LESS_EQUAL,
            State.ACCEPT_LSHIFT,
            State.ACCEPT_LSHIFT_ASSIGN,
            State.ACCEPT_GREATER,
            State.ACCEPT_GREATER_EQUAL,
            State.ACCEPT_RSHIFT,
            State.ACCEPT_RSHIFT_ASSIGN,
            State.ACCEPT_AND,
            State.ACCEPT_AND_ASSIGN,
            State.ACCEPT_OR,
            State.ACCEPT_OR_ASSIGN,
            State.ACCEPT_XOR,
            State.ACCEPT_XOR_ASSIGN,
            State.ACCEPT_NOT,
            State.ACCEPT_COLON,
            State.ACCEPT_ASSIGN1,
            State.ACCEPT_ASSIGN2,
            State.ACCEPT_NOT_EQUAL,
            State.ACCEPT_LPAREN,
            State.ACCEPT_RPAREN,
            State.ACCEPT_LBRACE,
            State.ACCEPT_RBRACE,
            State.ACCEPT_LBRACKET,
            State.ACCEPT_RBRACKET,
            State.ACCEPT_COMMA,
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
                Symbol.ZERO: State.IN_ZERO,
                Symbol.NUMBER: State.IN_DECIMAL,
                Symbol.EQUAL: State.IN_EQUAL,
                Symbol.PLUS: State.IN_PLUS,
                Symbol.MINUS: State.IN_MINUS,
                Symbol.ASTERISK: State.IN_MULTIPLICATION,
                Symbol.SLASH: State.IN_DIVISION,
                Symbol.MODULUS: State.IN_MODULUS,
                Symbol.LESS: State.IN_LESS,
                Symbol.GREATER: State.IN_GREATER,
                Symbol.AMPERSAND: State.IN_AND,
                Symbol.PIPE: State.IN_OR,
                Symbol.CARET: State.IN_XOR,
                Symbol.TILDE: State.ACCEPT_NOT,
                Symbol.COLON: State.IN_ASSIGN,
                Symbol.BANG: State.IN_NOT,
                Symbol.LPAREN: State.ACCEPT_LPAREN,
                Symbol.RPAREN: State.ACCEPT_RPAREN,
                Symbol.LBRACE: State.ACCEPT_LBRACE,
                Symbol.RBRACE: State.ACCEPT_RBRACE,
                Symbol.LBRACKET: State.ACCEPT_LBRACKET,
                Symbol.RBRACKET: State.ACCEPT_RBRACKET,
                Symbol.COMMA: State.ACCEPT_COMMA,
                Symbol.PERIOD: State.ACCEPT_PERIOD,
                Symbol.SEMICOLON: State.ACCEPT_SEMICOLON,
                Symbol.SINGLE_QUOT: State.IN_STRING1,
                Symbol.DOUBLE_QUOT: State.IN_STRING2,
                Symbol.SPACE: State.ACCEPT_SPACE,
                Symbol.NEWLINE: State.ACCEPT_NEWLINE,
            },
            State.IN_ID: {
                Symbol.LETTER: State.IN_ID,
                Symbol.DIGIT: State.IN_ID,
                Symbol.OTHER: State.ACCEPT_ID
            },
            State.IN_ZERO: {  # 0
                Symbol.OTHER: State.ACCEPT_ZERO,  # 0
                Symbol.OCTAL: State.IN_OCTAL,     # 0[0-7]
                Symbol.PREFIX_X: State.IN_HEX     # 0[xX]
            },
            State.IN_DECIMAL: {  # [1-9][0-9]
                Symbol.DIGIT: State.IN_DECIMAL,     # [1-9][0-9]+
                Symbol.OTHER: State.ACCEPT_DECIMAL  # [1-9][0-9]*
            },
            State.IN_OCTAL: {  # 0[0-7]
                Symbol.OCTAL: State.IN_OCTAL,       # 0[0-7]+
                Symbol.OTHER: State.ACCEPT_OCTAL    # 0[0-7]+
            },
            State.IN_HEX: {  # 0x
                Symbol.HEX: State.IN_HEX,           # 0[xX][0-9a-fA-F]+
                Symbol.OTHER: State.ACCEPT_HEX      # 0[xX][0-9a-fA-F]+
            },
            State.IN_PLUS: {  # +
                Symbol.EQUAL: State.ACCEPT_ADD_ASSIGN,  # +=
                Symbol.OTHER: State.ACCEPT_PLUS         # +
            },
            State.IN_MINUS: {  # -
                Symbol.EQUAL: State.ACCEPT_SUB_ASSIGN,          # -=
                Symbol.GREATER: State.ACCEPT_FUNC_ANNOTATION,   # ->
                Symbol.OTHER: State.ACCEPT_MINUS                # -
            },
            State.IN_MULTIPLICATION: {  # *
                Symbol.ASTERISK: State.IN_EXP,                      # **
                Symbol.EQUAL: State.ACCEPT_MULTIPLICATION_ASSIGN,   # *=
                Symbol.OTHER: State.ACCEPT_MULTIPLICATION           # *
            },
            State.IN_EXP: {  # **
                Symbol.EQUAL: State.ACCEPT_EXP_ASSIGN,  # **=
                Symbol.OTHER: State.ACCEPT_EXP          # **
            },
            State.IN_DIVISION: {  # /
                Symbol.SLASH: State.IN_FLOOR_DIV,            # //
                Symbol.EQUAL: State.ACCEPT_DIVISION_ASSIGN,  # /=
                Symbol.OTHER: State.ACCEPT_DIVISION          # /
            },
            State.IN_FLOOR_DIV: {  # //
                Symbol.EQUAL: State.ACCEPT_FLOOR_DIV_ASSIGN,  # //=
                Symbol.OTHER: State.ACCEPT_FLOOR_DIV          # //
            },
            State.IN_MODULUS: {  # %
                Symbol.EQUAL: State.ACCEPT_MODULUS_ASSIGN,  # %=
                Symbol.OTHER: State.ACCEPT_MODULUS          # %
            },
            State.IN_LESS: {  # <
                Symbol.LESS: State.IN_LSHIFT,           # <<
                Symbol.EQUAL: State.ACCEPT_LESS_EQUAL,  # <=
                Symbol.OTHER: State.ACCEPT_LESS         # <
            },
            State.IN_LSHIFT: {  # <<
                Symbol.EQUAL: State.ACCEPT_LSHIFT_ASSIGN,  # <<=
                Symbol.OTHER: State.ACCEPT_LSHIFT          # <<
            },
            State.IN_GREATER: {  # >
                Symbol.GREATER: State.IN_RSHIFT,           # >>
                Symbol.EQUAL: State.ACCEPT_GREATER_EQUAL,  # >=
                Symbol.OTHER: State.ACCEPT_GREATER         # >
            },
            State.IN_RSHIFT: {  # >>
                Symbol.EQUAL: State.ACCEPT_RSHIFT_ASSIGN,  # >>=
                Symbol.OTHER: State.ACCEPT_RSHIFT          # >>
            },
            State.IN_AND: {  # &
                Symbol.EQUAL: State.ACCEPT_AND_ASSIGN,  # &=
                Symbol.OTHER: State.ACCEPT_AND          # &
            },
            State.IN_OR: {  # |
                Symbol.EQUAL: State.ACCEPT_OR_ASSIGN,  # |=
                Symbol.OTHER: State.ACCEPT_OR          # |
            },
            State.IN_XOR: {
                Symbol.EQUAL: State.ACCEPT_XOR_ASSIGN,  # ^=
                Symbol.OTHER: State.ACCEPT_XOR          # ^
            },
            State.IN_ASSIGN: {  # :
                Symbol.EQUAL: State.ACCEPT_ASSIGN1,      # :=
                Symbol.OTHER: State.ACCEPT_COLON         # :
            },
            State.IN_EQUAL: {  # =
                Symbol.EQUAL: State.ACCEPT_EQUAL,       # ==
                Symbol.OTHER: State.ACCEPT_ASSIGN2      # =
            },
            State.IN_NOT: {  # !
                Symbol.EQUAL: State.ACCEPT_NOT_EQUAL  # !=
            },
            State.IN_STRING1: {  # '
                Symbol.LETTER: State.IN_STRING1,          # '[^\"\']
                Symbol.SINGLE_QUOT: State.ACCEPT_STRING1  # '[^\"\']'
            },
            State.IN_STRING2: {  # "
                Symbol.LETTER: State.IN_STRING2,          # "[^\"\']
                Symbol.DOUBLE_QUOT: State.ACCEPT_STRING2  # "[^\"\']"
            }
        }
        self.keywords = [
            'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise',
            'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try',
            'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with',
            'async', 'elif', 'if', 'or', 'yield'
        ]

    # State transition for input symbols.
    def progress(self, symbols):
        global error_occurred, error_msg

        for symbol in symbols:
            try:
                current_symbol = identify_symbol(symbol, self.currentState)

                if current_symbol != Symbol.OTHER:
                    self.lexeme += symbol

                self.currentState = self.table[self.currentState][current_symbol]

                # Check if accepted.
                check_acceptance(self, self.currentState)

                if current_symbol == Symbol.OTHER:
                    current_symbol = identify_symbol(symbol, self.currentState)
                    self.lexeme += symbol
                    self.currentState = self.table[self.currentState][current_symbol]
                    check_acceptance(self, self.currentState)
            except KeyError:
                error_occurred = True
                error_msg = "\n!!! Error occurred because of the symbol {} !!!\n".format(symbol)
                # print(error_msg)
                break


# Check if lexeme belongs to keyword.
def check_keyword(self, lexeme: str):
    if lexeme in self.keywords:
        return self.keywords.index(lexeme)
    return None


# Generate token
def make_token(self, state: State):
    token = CurrentToken()
    if state == State.ACCEPT_ID:
        # Check if lexeme belongs a keyword.
        key_num = check_keyword(self, self.lexeme)
        if key_num:
            token.set_token(key_num)
        else:
            token.set_token(Token.ID)
            value = insert_symbol_table(self.lexeme)
            token.set_token_value(value + 1)
    elif state == State.ACCEPT_EQUAL:
        token.set_token(Token.EQUAL)
    elif state == State.ACCEPT_ZERO:
        token.set_token(Token.ZERO)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_DECIMAL:
        token.set_token(Token.DECIMAL)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_OCTAL:
        token.set_token(Token.OCTAL)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_HEX:
        token.set_token(Token.HEX)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_PLUS:
        token.set_token(Token.PLUS)
    elif state == State.ACCEPT_ADD_ASSIGN:
        token.set_token(Token.ADD_ASSIGN)
    elif state == State.ACCEPT_MINUS:
        token.set_token(Token.MINUS)
    elif state == State.ACCEPT_SUB_ASSIGN:
        token.set_token(Token.SUB_ASSIGN)
    elif state == State.ACCEPT_FUNC_ANNOTATION:
        token.set_token(Token.FUNC_ANNOTATION)
    elif state == State.ACCEPT_MULTIPLICATION:
        token.set_token(Token.MULTIPLICATION)
    elif state == State.ACCEPT_MULTIPLICATION_ASSIGN:
        token.set_token(Token.MULTIPLICATION_ASSIGN)
    elif state == State.ACCEPT_EXP:
        token.set_token(Token.EXP)
    elif state == State.ACCEPT_EXP_ASSIGN:
        token.set_token(Token.EXP_ASSIGN)
    elif state == State.ACCEPT_DIVISION:
        token.set_token(Token.DIVISION)
    elif state == State.ACCEPT_DIVISION_ASSIGN:
        token.set_token(Token.DIV_ASSIGN)
    elif state == State.ACCEPT_FLOOR_DIV:
        token.set_token(Token.FLOOR_DIVISION)
    elif state == State.ACCEPT_FLOOR_DIV_ASSIGN:
        token.set_token(Token.FLOOR_DIV_ASSIGN)
    elif state == State.ACCEPT_MODULUS:
        token.set_token(Token.MODULUS)
    elif state == State.ACCEPT_MODULUS_ASSIGN:
        token.set_token(Token.MODULUS_ASSIGN)
    elif state == State.ACCEPT_LESS:
        token.set_token(Token.LESS)
    elif state == State.ACCEPT_LESS_EQUAL:
        token.set_token(Token.LESS_EQUAL)
    elif state == State.ACCEPT_LSHIFT:
        token.set_token(Token.LSHIFT)
    elif state == State.ACCEPT_LSHIFT_ASSIGN:
        token.set_token(Token.LSHIFT_ASSIGN)
    elif state == State.ACCEPT_GREATER:
        token.set_token(Token.GREATER)
    elif state == State.ACCEPT_GREATER_EQUAL:
        token.set_token(Token.GREATER_EQUAL)
    elif state == State.ACCEPT_RSHIFT:
        token.set_token(Token.RSHIFT)
    elif state == State.ACCEPT_RSHIFT_ASSIGN:
        token.set_token(Token.RSHIFT_ASSIGN)
    elif state == State.ACCEPT_AND:
        token.set_token(Token.AND)
    elif state == State.ACCEPT_AND_ASSIGN:
        token.set_token(Token.AND_ASSIGN)
    elif state == State.ACCEPT_OR:
        token.set_token(Token.OR)
    elif state == State.ACCEPT_OR_ASSIGN:
        token.set_token(Token.OR_ASSIGN)
    elif state == State.ACCEPT_XOR:
        token.set_token(Token.XOR)
    elif state == State.ACCEPT_XOR_ASSIGN:
        token.set_token(Token.XOR_ASSIGN)
    elif state == State.ACCEPT_NOT:
        token.set_token(Token.NOT)
    elif state == State.ACCEPT_COLON:
        token.set_token(Token.COLON)
    elif state == State.ACCEPT_ASSIGN1:
        token.set_token(Token.ASSIGN1)
    elif state == State.ACCEPT_ASSIGN2:
        token.set_token(Token.ASSIGN2)
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
    elif state == State.ACCEPT_COMMA:
        token.set_token(Token.COMMA)
    elif state == State.ACCEPT_PERIOD:
        token.set_token(Token.PERIOD)
    elif state == State.ACCEPT_SEMICOLON:
        token.set_token(Token.SEMICOLON)
    elif state == State.ACCEPT_STRING1:
        token.set_token(Token.STRING1)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_STRING2:
        token.set_token(Token.STRING2)
        value = insert_literal_table(self.lexeme)
        token.set_token_value(value + 1)
    elif state == State.ACCEPT_SPACE:
        token.set_token(Token.SPACE)
    elif state == State.ACCEPT_NEWLINE:
        token.set_token(Token.NEWLINE)

    token_table.add_token(token)
    # print(self.lexeme.strip(), token.get_token(), token.get_token_value())

    # Initialize state and lexeme.
    self.currentState = State.START
    self.lexeme = ''


# Check if state is accepted.
def check_acceptance(self, state: State):
    # If accepted, then create a token.
    if state in self.finalStates:
        make_token(self, state)


def main():
    # Read input-file source code.
    with open(sys.argv[1], "r") as source_code:
        code = source_code.read()
    source_code.close()

    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.progress(code)

    # Write analysis result to output-file.
    with open(sys.argv[2], "w") as output:
        output.write("==========================[ Token Table ]==========================\n")
        output.write(token_table.get_all_tokens())
        global error_occurred, error_msg
        if error_occurred:
            output.write(error_msg)
        output.write("\n==========================[ Symbol Table ]=========================\n")
        output.write(symbol_table.get_all_symbols())
        output.write("\n=========================[ Literal Table ]=========================\n")
        output.write(literal_table.get_all_literals())
    output.close()
    print('programmed by JeongHyeon Lee')


if __name__ == '__main__':
    main()
