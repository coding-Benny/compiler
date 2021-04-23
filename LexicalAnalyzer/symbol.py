from enum import Enum, auto
from dataclasses import dataclass
import re
from state import STATE


@dataclass
class SymbolTable:
    szSymbol: list
    nSymbol: int = 0


class SYMBOL(Enum):
    sb_letter = auto()
    sb_digit = auto()
    sb_equal = auto()               # =
    sb_less = auto()                # <
    sb_greater = auto()             # >
    sb_plus = auto()                # +
    sb_minus = auto()               # -
    sb_multiplication = auto()      # *
    sb_division = auto()            # /
    sb_modulus = auto()             # %
    sb_and = auto()                 # &
    sb_or = auto()                  # |
    sb_xor = auto()                 # ^
    sb_tilde = auto()               # ~
    sb_exclamation = auto()         # !
    sb_lparen = auto()              # (
    sb_rparen = auto()              # )
    sb_lbrace = auto()              # {
    sb_rbrace = auto()              # }
    sb_lbracket = auto()            # [
    sb_rbracket = auto()            # ]
    sb_comma = auto()               # ,
    sb_period = auto()              # .
    sb_colon = auto()               # :
    sb_semicolon = auto()           # ;
    sb_hash = auto()                # #
    sb_backslash = auto()           # \
    sb_single_quot = auto()         # '
    sb_double_quot = auto()         # "
    sb_at = auto()                  # @
    sb_other = auto()               # [^a-zA-Z0-9]


symbol_list = []
my_symbol_table = SymbolTable(szSymbol=symbol_list)


def match_symbol(character, status):
    cur_sb = None

    if bool(re.match('[a-zA-Z]', character)):
        cur_sb = SYMBOL.sb_letter
    elif bool(re.match('[0-9]', character)):
        cur_sb = SYMBOL.sb_digit
    if status == STATE.S_in_id:  # identifier other
        if bool(re.match('[^0-9a-zA-Z]', character)):
            cur_sb = SYMBOL.sb_other
    elif status == STATE.S_in_string1 or status == STATE.S_in_string2:  # string
        if bool(re.match('[^\"\']', character)):
            cur_sb = SYMBOL.sb_letter
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
    elif character.isspace():
        cur_sb = SYMBOL.sb_other
    return cur_sb

def insert_symbol_table(lexeme: str):
    for i in range(my_symbol_table.nSymbol):
        if my_symbol_table.szSymbol[i] == lexeme:
            return i
    my_symbol_table.szSymbol.append(lexeme)
    my_symbol_table.nSymbol += 1
    return my_symbol_table.nSymbol - 1