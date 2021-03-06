from enum import Enum, auto
import re
from state import State


class Symbol(Enum):
    LETTER = auto()         # [a-zA-Z_]
    ZERO = auto()           # 0
    NUMBER = auto()         # [1-9]
    DIGIT = auto()          # [0-9]
    OCTAL = auto()          # [0-7]
    HEX = auto()            # [0-9a-fA-F]
    PREFIX_X = auto()       # x, X
    EQUAL = auto()          # =
    LESS = auto()           # <
    GREATER = auto()        # >
    PLUS = auto()           # +
    MINUS = auto()          # -
    ASTERISK = auto()       # *
    SLASH = auto()          # /
    MODULUS = auto()        # %
    AMPERSAND = auto()      # &
    PIPE = auto()           # |
    CARET = auto()          # ^
    TILDE = auto()          # ~
    BANG = auto()           # !
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    COMMA = auto()          # ,
    PERIOD = auto()         # .
    COLON = auto()          # :
    SEMICOLON = auto()      # ;
    BACKSLASH = auto()      # \
    SINGLE_QUOT = auto()    # '
    DOUBLE_QUOT = auto()    # "
    SPACE = auto()          # ' '
    NEWLINE = auto()        # \n
    OTHER = auto()          # It depends on the condition.


class SymbolTable:
    def __init__(self):
        self.__szSymbol: list = []

    def add_symbol(self, s: str):
        self.__szSymbol.append(s)

    def check_symbol(self, s: str):
        if s in self.__szSymbol:
            return self.__szSymbol.index(s)
        else:
            return -1

    def number_of_symbols(self):
        return len(self.__szSymbol)

    def get_all_symbols(self):
        res = ''
        for i, symbol in enumerate(self.__szSymbol):
            res += '({}) {}\n'.format(i + 1, symbol)
        return res

    def get_symbol_table(self):
        return self.__szSymbol


symbol_table = SymbolTable()


def identify_symbol(character, status):
    cur_sb = None

    if bool(re.match('[a-zA-Z_]', character)):
        cur_sb = Symbol.LETTER

    if status == State.START:
        if character == '0':
            cur_sb = Symbol.ZERO
        elif bool(re.match('[1-9]', character)):
            cur_sb = Symbol.NUMBER
        elif character == '+':
            cur_sb = Symbol.PLUS
        elif character == '-':
            cur_sb = Symbol.MINUS
        elif character == '*':
            cur_sb = Symbol.ASTERISK
        elif character == '/':
            cur_sb = Symbol.SLASH
        elif character == '%':
            cur_sb = Symbol.MODULUS
        elif character == '=':
            cur_sb = Symbol.EQUAL
        elif character == '>':
            cur_sb = Symbol.GREATER
        elif character == '<':
            cur_sb = Symbol.LESS
        elif character == '&':
            cur_sb = Symbol.AMPERSAND
        elif character == '|':
            cur_sb = Symbol.PIPE
        elif character == '^':
            cur_sb = Symbol.CARET
        elif character == '~':
            cur_sb = Symbol.TILDE
        elif character == ':':
            cur_sb = Symbol.COLON
        elif character == ';':
            cur_sb = Symbol.SEMICOLON
        elif character == '!':
            cur_sb = Symbol.BANG
        elif character == '@':
            cur_sb = Symbol.AT
        elif character == '.':
            cur_sb = Symbol.PERIOD
        elif character == ',':
            cur_sb = Symbol.COMMA
        elif character == '\'':
            cur_sb = Symbol.SINGLE_QUOT
        elif character == '\"':
            cur_sb = Symbol.DOUBLE_QUOT
        elif character == '(':
            cur_sb = Symbol.LPAREN
        elif character == ')':
            cur_sb = Symbol.RPAREN
        elif character == '{':
            cur_sb = Symbol.LBRACE
        elif character == '}':
            cur_sb = Symbol.RBRACE
        elif character == '[':
            cur_sb = Symbol.LBRACKET
        elif character == ']':
            cur_sb = Symbol.RBRACKET
        elif character == ' ' or character == '\t':
            cur_sb = Symbol.SPACE
        elif character == '\n':
            cur_sb = Symbol.NEWLINE

    if status == State.IN_ID:  # identifier other
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.DIGIT
        elif bool(re.match('[^0-9a-zA-Z_]', character)):
            cur_sb = Symbol.OTHER
    elif status == State.IN_ZERO:
        if character.lower() == 'x':
            cur_sb = Symbol.PREFIX_X
        elif bool(re.match('[0-7]', character)):
            cur_sb = Symbol.OCTAL
        else:
            cur_sb = Symbol.OTHER
    elif status == State.IN_DECIMAL:
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.DIGIT
        elif bool(re.match('[^0-9]', character)):
            cur_sb = Symbol.OTHER
    elif status == State.IN_OCTAL:
        if bool(re.match('[0-7]', character)):
            cur_sb = Symbol.OCTAL
        else:
            cur_sb = Symbol.OTHER
    elif status == State.IN_HEX:
        if bool(re.match('[0-9a-fA-F]', character)):
            cur_sb = Symbol.HEX
        else:
            cur_sb = Symbol.OTHER
    elif status == State.IN_STRING1 or status == State.IN_STRING2:  # string
        if bool(re.match('[^\"\']', character)):
            cur_sb = Symbol.LETTER
        elif character == '\'':
            cur_sb = Symbol.SINGLE_QUOT
        elif character == '\"':
            cur_sb = Symbol.DOUBLE_QUOT
    elif status == State.IN_MINUS:
        if character != '>' and character != '=':
            cur_sb = Symbol.OTHER
        elif character == '>':
            cur_sb = Symbol.GREATER
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status == State.IN_MULTIPLICATION:
        if character != '*' and character != '=':
            cur_sb = Symbol.OTHER
        elif character == '*':
            cur_sb = Symbol.ASTERISK
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status == State.IN_DIVISION:
        if character != '/' and character != '=':
            cur_sb = Symbol.OTHER
        elif character == '/':
            cur_sb = Symbol.SLASH
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status == State.IN_LESS:
        if character != '<' and character != '=':
            cur_sb = Symbol.OTHER
        elif character == '<':
            cur_sb = Symbol.LESS
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status == State.IN_GREATER:
        if character != '>' and character != '=':
            cur_sb = Symbol.OTHER
        elif character == '>':
            cur_sb = Symbol.GREATER
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status in [State.IN_ASSIGN, State.IN_EQUAL, State.IN_PLUS, State.IN_EXP, State.IN_FLOOR_DIV,
                    State.IN_MODULUS, State.IN_LSHIFT, State.IN_RSHIFT, State.IN_AND, State.IN_OR, State.IN_XOR,
                    State.IN_ASSIGN, State.IN_EQUAL]:
        if character != '=':
            cur_sb = Symbol.OTHER
        else:
            cur_sb = Symbol.EQUAL

    return cur_sb


def insert_symbol_table(lexeme: str):
    check = symbol_table.check_symbol(lexeme)
    if check == -1:
        symbol_table.add_symbol(lexeme)
    return symbol_table.get_symbol_table().index(lexeme)
