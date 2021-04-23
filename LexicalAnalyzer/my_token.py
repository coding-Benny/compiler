from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class Token:
    number: int
    value: int


class TOKEN(Enum):
    Token_id = auto()
    Token_decimal = auto()
    Token_zero = auto()
    Token_octal = auto()
    Token_hex = auto()
    Token_string1 = auto()
    Token_string2 = auto()
    Token_plus = auto()  # +
    Token_add_assign = auto()  # +=
    Token_minus = auto()  # -
    Token_func_annotation = auto()  # ->
    Token_sub_assign = auto()  # -=
    Token_mult = auto()  # *
    Token_exp = auto()  # **
    Token_mult_assign = auto()  # *=
    Token_exp_assign = auto()  # **=
    Token_div = auto()  # /
    Token_floor_div = auto()  # //
    Token_div_assign = auto()  # /=
    Token_floor_div_assign = auto()  # //=
    Token_modulus = auto()  # %
    Token_modulus_assign = auto()  # %=
    Token_less = auto()  # <
    Token_less_equal = auto()  # <=
    Token_left_shift = auto()  # <<
    Token_left_shift_assign = auto()  # <<=
    Token_greater = auto()  # >
    Token_greater_equal = auto()  # >=
    Token_right_shift = auto()  # >>
    Token_right_shift_assign = auto()  # >>=
    Token_and = auto()  # &
    Token_and_assign = auto()  # &=
    Token_or = auto()  # |
    Token_or_assign = auto()  # \=
    Token_xor = auto()  # ^
    Token_xor_assign = auto()  # ^=
    Token_not = auto()  # ~
    Token_colon = auto()  # :
    Token_assign1 = auto()  # :=
    Token_assign2 = auto()  # =
    Token_equal = auto()  # ==
    Token_not_equal = auto()  # !=
    Token_left_paren = auto()  # (
    Token_right_paren = auto()  # )
    Token_left_brace = auto()  # {
    Token_right_brace = auto()  # }
    Token_left_bracket = auto()  # [
    Token_right_bracket = auto()  # ]
    Token_comma = auto()  # ,
    Token_period = auto()  # .
    Token_semicolon = auto()  # ;
    Token_comment = auto()  # #
