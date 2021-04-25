class LiteralTable:
    def __init__(self):
        self.__szLiteral: list = []

    def add_literal(self, s: str):
        self.__szLiteral.append(s)

    def check_literal(self, s: str):
        for i, literal in enumerate(self.__szLiteral):
            if literal == s:
                return i
        return -1

    def number_of_literals(self):
        return len(self.__szLiteral)

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
