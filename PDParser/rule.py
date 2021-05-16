class Rule:
    def __init__(self, s: str):
        rule = s.replace(' ', '').split('→')
        self.__RHS = rule[1]

    def get_a_RHS(self, idx: int):
        return self.__RHS[idx]

    def get_RHS(self):
        return self.__RHS
