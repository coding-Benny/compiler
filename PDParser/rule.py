class Rule:
    def __init__(self, no: int, s: str):
        rule = s.replace(' ', '').split('→')
        self.id = no
        self.LHS = rule[0]
        self.RHS = rule[1]

    def get_id(self):
        return self.id

    def get_RHS_len(self):
        return len(self.RHS)

    def get_a_RHS(self, idx: int):
        return self.RHS[idx]

    def get_RHS(self):
        return self.RHS

    def get_LHS(self):
        return self.LHS
