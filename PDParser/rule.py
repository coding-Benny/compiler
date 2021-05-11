class Rule:
    def __init__(self, s: str):
        rule = s.replace(' ', '').split('→')
        self.LHS = rule[0]
        self.RHS = rule[1]

    def get_RHS_len(self):
        return len(self.RHS)

    def get_a_RHS(self, idx: int):
        return self.RHS[idx]

    def get_RHS(self):
        return self.RHS

    def get_LHS_len(self):
        return len(self.LHS)

    def get_a_LHS(self, idx: int):
        return self.LHS[idx]

    def get_LHS(self):
        return self.LHS
