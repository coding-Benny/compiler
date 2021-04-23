from enum import Enum, auto
from dataclasses import dataclass
import re
from state import STATE


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
    sb_letter = auto()
    sb_zero = auto()
    sb_number = auto()
    sb_digit = auto()
    sb_equal = auto()  # =
    sb_less = auto()  # <
    sb_greater = auto()  # >
    sb_plus = auto()  # +
    sb_minus = auto()  # -
    sb_multiplication = auto()  # *
    sb_division = auto()  # /
    sb_modulus = auto()  # %
    sb_and = auto()  # &
    sb_or = auto()  # |
    sb_xor = auto()  # ^
    sb_tilde = auto()  # ~
    sb_exclamation = auto()  # !
    sb_lparen = auto()  # (
    sb_rparen = auto()  # )
    sb_lbrace = auto()  # {
    sb_rbrace = auto()  # }
    sb_lbracket = auto()  # [
    sb_rbracket = auto()  # ]
    sb_comma = auto()  # ,
    sb_period = auto()  # .
    sb_colon = auto()  # :
    sb_semicolon = auto()  # ;
    sb_hash = auto()  # #
    sb_backslash = auto()  # \
    sb_single_quot = auto()  # '
    sb_double_quot = auto()  # "
    sb_at = auto()  # @
    sb_other = auto()  # [^a-zA-Z0-9]
    sb_space = auto()


symbol_table = SymbolTable()


def identify_symbol(character, status):
    cur_sb = None

    if bool(re.match('[a-zA-Z]', character)):
        cur_sb = Symbol.sb_letter

    if status == STATE.S_start:
        if character == '0':
            cur_sb = Symbol.sb_zero
        elif bool(re.match('[1-9]', character)):
            cur_sb = Symbol.sb_number

    if status == STATE.S_in_id:  # identifier other
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.sb_digit
        if bool(re.match('[^0-9a-zA-Z]', character)):
            cur_sb = Symbol.sb_other
    elif status == STATE.S_in_decimal:
        if bool(re.match('[0-9]', character)):
            cur_sb = Symbol.sb_digit
        elif bool(re.match('[^0-9]', character)):
            cur_sb = Symbol.sb_other
    elif status == STATE.S_in_string1 or status == STATE.S_in_string2:  # string
        if bool(re.match('[^\"\']', character)):
            cur_sb = Symbol.sb_letter
        elif character == '\'':
            cur_sb = Symbol.sb_single_quot
        elif character == '\"':
            cur_sb = Symbol.sb_double_quot
    elif status == STATE.S_in_assign or status == STATE.S_in_equal:
        if character != '=':
            cur_sb = Symbol.sb_other
    elif character == '+':
        cur_sb = Symbol.sb_plus
    elif character == '-':
        cur_sb = Symbol.sb_minus
    elif character == '*':
        cur_sb = Symbol.sb_multiplication
    elif character == '/':
        cur_sb = Symbol.sb_division
    elif character == '%':
        cur_sb = Symbol.sb_modulus
    elif character == '=':
        cur_sb = Symbol.sb_equal
    elif character == '>':
        cur_sb = Symbol.sb_greater
    elif character == '<':
        cur_sb = Symbol.sb_less
    elif character == '&':
        cur_sb = Symbol.sb_and
    elif character == '|':
        cur_sb = Symbol.sb_or
    elif character == '^':
        cur_sb = Symbol.sb_xor
    elif character == '~':
        cur_sb = Symbol.sb_tilde
    elif character == ':':
        cur_sb = Symbol.sb_colon
    elif character == ';':
        cur_sb = Symbol.sb_semicolon
    elif character == '!':
        cur_sb = Symbol.sb_exclamation
    elif character == '@':
        cur_sb = Symbol.sb_at
    elif character == '.':
        cur_sb = Symbol.sb_period
    elif character == ',':
        cur_sb = Symbol.sb_comma
    elif character == '\'':
        cur_sb = Symbol.sb_single_quot
    elif character == '\"':
        cur_sb = Symbol.sb_double_quot
    elif character == '(':
        cur_sb = Symbol.sb_lparen
    elif character == ')':
        cur_sb = Symbol.sb_rparen
    elif character == '{':
        cur_sb = Symbol.sb_lbrace
    elif character == '}':
        cur_sb = Symbol.sb_rbrace
    elif character == '[':
        cur_sb = Symbol.sb_lbracket
    elif character == ']':
        cur_sb = Symbol.sb_rbracket
    elif character.isspace():
        cur_sb = Symbol.sb_space
    return cur_sb


def insert_symbol_table(lexeme: str):
    check = symbol_table.check_symbol(lexeme)
    if check == -1:
        symbol_table.add_symbol(lexeme)
    return symbol_table.number_of_symbols() - 1
