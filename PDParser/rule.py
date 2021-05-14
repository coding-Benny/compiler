class Rule:
    def __init__(self, no: int, s: str):
        rule = s.replace(' ', '').split('→')
        self.__id = no
        self.__LHS = rule[0]
        self.__RHS = rule[1]

    def get_id(self):
        return self.__id

    def get_RHS_len(self):
        return len(self.__RHS)

    def get_a_RHS(self, idx: int):
        return self.__RHS[idx]

    def get_RHS(self):
        return self.__RHS

    def get_LHS(self):
        return self.__LHS
