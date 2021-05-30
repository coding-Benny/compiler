from collections import defaultdict


class ActionTable:
    def __init__(self):
        self.__table = defaultdict(dict)

    def insert_action(self, r: int, c: int, a: str):
        self.__table[r][c] = a

    def get_action_from_action_table(self, r: int, c: int):
        return self.__table[r][c]


class GotoTable:
    def __init__(self):
        self.__table = defaultdict(dict)

    def insert_goto_state(self, r: int, c: int, n: int):
        self.__table[r][c] = n

    def get_goto_state(self, r: int, c: int):
        return self.__table[r][c]
