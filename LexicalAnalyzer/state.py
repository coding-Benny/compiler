from enum import Enum, auto


class State(Enum):
    # start state
    START = auto()
    # escape state for escape sequence(in string)
    ESCAPE = auto()                       # \
    # processing states
    IN_ID = auto()
    IN_DECIMAL = auto()
    IN_HEX = auto()
    IN_STRING1 = auto()                   # '
    IN_STRING2 = auto()                   # "
    IN_PLUS = auto()                      # +
    IN_MINUS = auto()                     # -
    IN_MULTIPLICATION = auto()            # *
    IN_EXP = auto()                       # **
    IN_DIVISION = auto()                  # /
    IN_FLOOR_DIV = auto()                 # //
    IN_MODULUS = auto()                   # %
    IN_LESS = auto()                      # <
    IN_GREATER = auto()                   # >
    IN_LSHIFT = auto()                    # <<
    IN_RSHIFT = auto()                    # >>
    IN_AND = auto()                       # &
    IN_OR = auto()                        # |
    IN_XOR = auto()                       # ^
    IN_ASSIGNMENT = auto()                # :
    IN_EQUAL = auto()                     # =
    IN_NOT = auto()                       # !
    # accept states
    ACCEPT_ID = auto()
    ACCEPT_DECIMAL = auto()
    ACCEPT_ZERO = auto()
    ACCEPT_OCTAL = auto()
    ACCEPT_HEX = auto()
    ACCEPT_STRING1 = auto()
    ACCEPT_STRING2 = auto()
    ACCEPT_PLUS = auto()                  # +
    ACCEPT_ADD_ASSIGNMENT = auto()        # +=
    ACCEPT_MINUS = auto()                 # -
    ACCEPT_FUNC_ANNOTATION = auto()       # ->
    ACCEPT_SUB_ASSIGNMENT = auto()        # -=
    ACCEPT_MULTIPLICATION = auto()        # *
    ACCEPT_EXP = auto()                   # **
    ACCEPT_MULTIPLICATION_ASSIGNMENT = auto()  # *=
    ACCEPT_EXP_ASSIGNMENT = auto()        # **=
    ACCEPT_DIVISION = auto()              # /
    ACCEPT_FLOOR_DIV = auto()             # //
    ACCEPT_DIVISION_ASSIGNMENT = auto()   # /=
    ACCEPT_FLOOR_DIV_ASSIGNMENT = auto()  # //=
    ACCEPT_MODULUS = auto()               # %
    ACCEPT_MODULUS_ASSIGNMENT = auto()    # %=
    ACCEPT_LESS = auto()                  # <
    ACCEPT_LESS_EQUAL = auto()            # <=
    ACCEPT_LSHIFT = auto()                # <<
    ACCEPT_LSHIFT_ASSIGNMENT = auto()     # <<=
    ACCEPT_GREATER = auto()               # >
    ACCEPT_GREATER_EQUAL = auto()         # >=
    ACCEPT_RSHIFT = auto()                # >>
    ACCEPT_RSHIFT_ASSIGNMENT = auto()     # >>=
    ACCEPT_AND = auto()                   # &
    ACCEPT_AND_ASSIGNMENT = auto()        # &=
    ACCEPT_OR = auto()                    # |
    ACCEPT_OR_ASSIGNMENT = auto()         # \=
    ACCEPT_XOR = auto()                   # ^
    ACCEPT_XOR_ASSIGNMENT = auto()        # ^=
    ACCEPT_NOT = auto()                   # ~
    ACCEPT_COLON = auto()                 # :
    ACCEPT_ASSIGNMENT1 = auto()           # :=
    ACCEPT_ASSIGNMENT2 = auto()           # =
    ACCEPT_EQUAL = auto()                 # ==
    ACCEPT_NOT_EQUAL = auto()             # !=
    ACCEPT_LPAREN = auto()                # (
    ACCEPT_RPAREN = auto()                # )
    ACCEPT_LBRACE = auto()                # {
    ACCEPT_RBRACE = auto()                # }
    ACCEPT_LBRACKET = auto()              # [
    ACCEPT_RBRACKET = auto()              # ]
    S_accept_comma = auto()               # ,
    ACCEPT_PERIOD = auto()                # .
    ACCEPT_SEMICOLON = auto()             # ;
    ACCEPT_COMMENT = auto()               # #
    ACCEPT_SPACE = auto()
