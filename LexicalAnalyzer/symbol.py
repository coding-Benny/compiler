from enum import Enum, auto
from dataclasses import dataclass


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
