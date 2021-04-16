from enum import Enum, auto


class STATE(Enum):
    # start state
    S_start = auto()
    # escape state for escape sequence(in string)
    S_escape = auto()                   # \
    # processing states
    S_in_id = auto()
    S_in_hex = auto()
    S_in_string = auto()
    S_in_plus = auto()                  # +
    S_in_minus = auto()                 # -
    S_in_multiplication = auto()        # *
    S_in_division = auto()              # /
    S_in_floor_div = auto()             # //
    S_in_modulus = auto()               # %
    S_in_less = auto()                  # <
    S_in_greater = auto()               # >
    S_in_and = auto()                   # &
    S_in_or = auto()                    # |
    S_in_xor = auto()                   # ^
    S_in_assign = auto()                # :
    S_in_equal = auto()                 # =
    S_in_not = auto()                   # !
    # accept states
    S_accept_id = auto()
    S_accept_decimal = auto()
    S_accept_zero = auto()
    S_accept_octal = auto()
    S_accept_hex = auto()
    S_accept_string = auto()
    S_accept_plus = auto()              # +
    S_accept_add_assign = auto()        # +=
    S_accept_minus = auto()             # -
    S_accept_func_annotation = auto()   # ->
    S_accept_sub_assign = auto()        # -=
    S_accept_mult = auto()              # *
    S_accept_exp = auto()               # **
    S_accept_mult_assign = auto()       # *=
    S_accept_exp_assign = auto()        # **=
    S_accept_div = auto()               # /
    S_accept_floor_div = auto()         # //
    S_accept_div_assign = auto()        # /=
    S_accept_floor_div_assign = auto()  # //=
    S_accept_modulus = auto()           # %
    S_accept_modulus_assign = auto()    # %=
    S_accept_less = auto()              # <
    S_accept_less_equal = auto()        # <=
    S_accept_left_shift = auto()        # <<
    S_accept_greater = auto()           # >
    S_accept_greater_equal = auto()     # >=
    S_accept_right_shift = auto()       # >>
    S_accept_and_assignment = auto()    # &=
    S_accept_or_assignment = auto()     # \=
    S_accept_xor_assignment = auto()    # ^=
    S_accept_not = auto()               # ~
    S_accept_colon = auto()             # :
    S_accept_assign1 = auto()           # :=
    S_accept_assign2 = auto()           # =
    S_accept_equal = auto()             # ==
    S_accept_not_equal = auto()         # !=
    S_accept_lparen = auto()            # (
    S_accept_rparen = auto()            # )
    S_accept_lbrace = auto()            # {
    S_accept_rbrace = auto()            # }
    S_accept_lbracket = auto()          # [
    S_accept_rbracket = auto()          # ]
    S_accept_comma = auto()             # ,
    S_accept_period = auto()            # .
    S_accept_semicolon = auto()         # ;
    S_accept_comment = auto()           # #
