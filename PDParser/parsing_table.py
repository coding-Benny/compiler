from rule import *
from collections import defaultdict


class ParsingTable:
    def __init__(self):
        self.__table = defaultdict(dict)

    def insert_rule(self, r: int, c: int, p: Rule):
        self.__table[r][c] = p.get_RHS()

    def get_rule(self, r: int, c: int):
        return self.__table[r][c]
