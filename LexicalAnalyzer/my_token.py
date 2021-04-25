from enum import Enum, auto


class Token(Enum):
    ID = auto()
    DECIMAL = auto()
    ZERO = auto()
    OCTAL = auto()
    HEX = auto()
    STRING1 = auto()
    STRING2 = auto()
    PLUS = auto()                       # +
    ADD_ASSIGN = auto()             # +=
    MINUS = auto()                      # -
    FUNC_ANNOTATION = auto()            # ->
    SUB_ASSIGN = auto()             # -=
    MULTIPLICATION = auto()             # *
    EXP = auto()                        # **
    MULTIPLICATION_ASSIGN = auto()  # *=
    EXP_ASSIGN = auto()             # **=
    DIVISION = auto()                   # /
    FLOOR_DIVISION = auto()             # //
    DIV_ASSIGN = auto()             # /=
    FLOOR_DIV_ASSIGN = auto()       # //=
    MODULUS = auto()                    # %
    MODULUS_ASSIGN = auto()         # %=
    LESS = auto()                       # <
    LESS_EQUAL = auto()                 # <=
    LSHIFT = auto()                     # <<
    LSHIFT_ASSIGN = auto()          # <<=
    GREATER = auto()                    # >
    GREATER_EQUAL = auto()              # >=
    RSHIFT = auto()                     # >>
    RSHIFT_ASSIGN = auto()          # >>=
    AND = auto()                        # &
    AND_ASSIGN = auto()             # &=
    OR = auto()                         # |
    OR_ASSIGN = auto()              # \=
    XOR = auto()                        # ^
    XOR_ASSIGN = auto()             # ^=
    NOT = auto()                        # ~
    COLON = auto()                      # :
    ASSIGN1 = auto()                # :=
    ASSIGN2 = auto()                # =
    EQUAL = auto()                      # ==
    NOT_EQUAL = auto()                  # !=
    LPAREN = auto()                     # (
    RPAREN = auto()                     # )
    LBRACE = auto()                     # {
    RBRACE = auto()                     # }
    LBRACKET = auto()                   # [
    RBRACKET = auto()                   # ]
    COMMA = auto()                      # ,
    PERIOD = auto()                     # .
    SEMICOLON = auto()                  # ;
    SPACE = auto()                      # ' '
    NEWLINE = auto()                    # \n


class CurrentToken:
    def __init__(self):
        self.__number: int = 0
        self.__value: int = 0

    def set_token(self, n: Token):
        self.__number = n

    def set_token_value(self, v: int):
        self.__value = v

    def get_token(self):
        return self.__number

    def get_token_value(self):
        if self.__value == 0:
            return '-'
        else:
            return self.__value


class TokenTable:
    def __init__(self):
        self.__pToken: list = []

    def add_token(self, p: CurrentToken):
        self.__pToken.append(p)

    def number_of_tokens(self):
        return len(self.__pToken)

    def get_all_tokens(self):
        res = ''
        for token in self.__pToken:
            if token.get_token() != Token.NEWLINE:
                res += '({}, {}) '.format(token.get_token(), token.get_token_value())
            else:
                res += '({}, {})\n'.format(token.get_token(), token.get_token_value())

        return res
