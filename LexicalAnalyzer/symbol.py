from enum import Enum, auto


class Symbol(Enum):
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
    sb_left_paren = auto()          # (
    sb_right_paren = auto()         # )
    sb_left_brace = auto()          # {
    sb_right_brace = auto()         # }
    sb_left_bracket = auto()        # [
    sb_right_bracket = auto()       # ]
    sb_comma = auto()               # ,
    sb_period = auto()              # .
    sb_colon = auto()               # :
    sb_semicolon = auto()           # ;
    sb_hash = auto()                # #
    sb_backslash = auto()           # \
    sb_single_quotation = auto()    # '
    sb_double_quotation = auto()    # "
    sb_at = auto()                  # @
