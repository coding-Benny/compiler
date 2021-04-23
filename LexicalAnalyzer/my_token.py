from enum import Enum, auto
from dataclasses import dataclass


class Token(Enum):
    ID = auto()
    DECIMAL = auto()
    ZERO = auto()
    OCTAL = auto()
    HEX = auto()
    STRING1 = auto()
    STRING2 = auto()
    PLUS = auto()  # +
    ADD_ASSIGNMENT = auto()  # +=
    MINUS = auto()  # -
    FUNC_ANNOTATION = auto()  # ->
    SUB_ASSIGNMENT = auto()  # -=
    MULTIPLICATION = auto()  # *
    EXP = auto()  # **
    MULTIPLICATION_ASSIGNMENT = auto()  # *=
    EXP_ASSIGNMENT = auto()  # **=
    DIVISION = auto()  # /
    FLOOR_DIVISION = auto()  # //
    DIV_ASSIGNMENT = auto()  # /=
    FLOOR_DIV_ASSIGNMENT = auto()  # //=
    MODULUS = auto()  # %
    MODULUS_ASSIGNMENT = auto()  # %=
    LESS = auto()  # <
    LESS_EQUAL = auto()  # <=
    LSHIFT = auto()  # <<
    LSHIFT_ASSIGNMENT = auto()  # <<=
    GREATER = auto()  # >
    GREATER_EQUAL = auto()  # >=
    RSHIFT = auto()  # >>
    RSHIFT_ASSIGNMENT = auto()  # >>=
    AND = auto()  # &
    AND_ASSIGNMENT = auto()  # &=
    OR = auto()  # |
    OR_ASSIGNMENT = auto()  # \=
    XOR = auto()  # ^
    XOR_ASSIGNMENT = auto()  # ^=
    NOT = auto()  # ~
    COLON = auto()  # :
    ASSIGNMENT1 = auto()  # :=
    ASSIGNMENT2 = auto()  # =
    EQUAL = auto()  # ==
    NOT_EQUAL = auto()  # !=
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COMMA = auto()  # ,
    PERIOD = auto()  # .
    SEMICOLON = auto()  # ;
    COMMENT = auto()  # #
    SPACE = auto()


@dataclass
class MyToken:
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
        return self.__value


@dataclass
class TokenTable:
    def __init__(self):
        self.__pToken: list = []
        self.__nToken: int = 0

    def add_token(self, p: MyToken):
        self.__pToken.append(p)
        self.__nToken += 1

    def number_of_tokens(self):
        return self.__nToken

    def get_all_tokens(self):
        res = ''
        for token in self.__pToken:
            if not token.get_token_value():
                token.set_token_value('-')
            res += '({}, {})\n'.format(token.get_token(), token.get_token_value())
        return res
