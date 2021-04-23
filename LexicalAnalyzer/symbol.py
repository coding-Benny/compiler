from enum import Enum, auto
from dataclasses import dataclass
import re
from state import State


@dataclass
class SymbolTable:
    def __init__(self):
        self.__szSymbol: list = []
        self.__nSymbol: int = 0

    def add_symbol(self, s: str):
        self.__szSymbol.append(s)
        self.__nSymbol += 1

    def check_symbol(self, s: str):
        for i, symbol in enumerate(self.__szSymbol):
            if symbol == s:
                return i
        return -1

    def number_of_symbols(self):
        return self.__nSymbol

    def get_all_symbols(self):
        res = ''
        for i, symbol in enumerate(self.__szSymbol):
            res += '({}) {}\n'.format(i + 1, symbol)
        return res


class Symbol(Enum):
    LETTER = auto()
    ZERO = auto()
    NUMBER = auto()
    DIGIT = auto()
    EQUAL = auto()  # =
    LESS = auto()  # <
    GREATER = auto()  # >
    PLUS = auto()  # +
    MINUS = auto()  # -
    ASTERISK = auto()  # *
    DIVISION = auto()  # /
    MODULUS = auto()  # %
    AMPERSAND = auto()  # &
    PIPE = auto()  # |
    CARET = auto()  # ^
    TILDE = auto()  # ~
    BANG = auto()  # !
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COMMA = auto()  # ,
    PERIOD = auto()  # .
    COLON = auto()  # :
    SEMICOLON = auto()  # ;
    HASH = auto()  # #
    BACKSLASH = auto()  # \
    SINGLE_QUOT = auto()  # '
    DOUBLE_QUOT = auto()  # "
    AT = auto()  # @
    OTHER = auto()  # [^a-zA-Z0-9]
    SPACE = auto()
    NEWLINE = auto()


symbol_table = SymbolTable()


def identify_symbol(character, status):
    cur_sb = None

    if bool(re.match('[a-zA-Z]', character)):
        cur_sb = Symbol.LETTER

    if status == State.START:
        if character == '0':
            cur_sb = Symbol.ZERO
        elif bool(re.match('[1-9]', character)):
            cur_sb = Symbol.NUMBER

    if status == State.IN_ID:  # identifier other
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.DIGIT
        if bool(re.match('[^0-9a-zA-Z]', character)):
            cur_sb = Symbol.OTHER
    elif status == State.IN_DECIMAL:
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.DIGIT
        elif bool(re.match('[^0-9]', character)):
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
            cur_sb = Symbol.DIVISION
        elif character == '=':
            cur_sb = Symbol.EQUAL
    elif status in [State.IN_ASSIGNMENT, State.IN_EQUAL, State.IN_PLUS, State.IN_EXP, State.IN_FLOOR_DIV,
                    State.IN_MODULUS, State.IN_LSHIFT, State.IN_RSHIFT, State.IN_AND, State.IN_OR, State.IN_XOR,
                    State.IN_ASSIGNMENT, State.IN_EQUAL]:
        if character != '=':
            cur_sb = Symbol.OTHER
        else:
            cur_sb = Symbol.EQUAL
    elif character == '+':
        cur_sb = Symbol.PLUS
    elif character == '-':
        cur_sb = Symbol.MINUS
    elif character == '*':
        cur_sb = Symbol.ASTERISK
    elif character == '/':
        cur_sb = Symbol.DIVISION
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
    return cur_sb


def insert_symbol_table(lexeme: str):
    check = symbol_table.check_symbol(lexeme)
    if check == -1:
        symbol_table.add_symbol(lexeme)
    return symbol_table.number_of_symbols() - 1
