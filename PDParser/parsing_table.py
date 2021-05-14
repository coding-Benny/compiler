from rule import *
from collections import defaultdict


class ParsingTable:
    def __init__(self):
        self.__table = defaultdict(dict)

    def insert_rule(self, p: Rule):
        self.__table[p.get_LHS()][p.get_a_RHS(0)] = p

    def get_rule(self, r: str, c: str):
        return self.__table[r][c]
