from dataclasses import dataclass


@dataclass
class LiteralTable:
    def __init__(self):
        self.__szLiteral: list = []
        self.__nLiteral: int = 0

    def add_literal(self, s: str):
        self.__szLiteral.append(s)
        self.__nLiteral += 1

    def check_literal(self, s: str):
        for i, literal in enumerate(self.__szLiteral):
            if literal == s:
                return i
        return -1

    def number_of_literals(self):
        return self.__nLiteral

    def get_all_literals(self):
        res = ''
        for i, literal in enumerate(self.__szLiteral):
            res += '({}) {}\n'.format(i + 1, literal)
        return res


literal_table = LiteralTable()


def insert_literal_table(lexeme: str):
    check = literal_table.check_literal(lexeme)
    if check == -1:
        literal_table.add_literal(lexeme)
    return literal_table.number_of_literals() - 1
