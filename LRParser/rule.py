from enum import Enum, auto

NonTerminal = Enum('NonTerminal', 'E T F')
Terminal = Enum('Terminal', 'a PLUS ASTERISK LPAREN RPAREN DOLLAR')
terminal_dict = {
    '+': 'PLUS',
    '*': 'ASTERISK',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '$': 'DOLLAR',
}


class Rule:
    def __init__(self, s: str):
        rule = s.replace(' ', '').split('→')
        self.__LHS = NonTerminal[rule[0]].name
        # RHS_list = []
        # for RHS in rule[1]:
        #     if RHS.isupper():
        #         RHS_list.append(NonTerminal[RHS].name)
        #     else:
        #         RHS_list.append(Terminal[terminal_dict.get(RHS)].name)
        self.__num_of_RHS = len(rule[1])

    def get_LHS(self):
        return self.__LHS

    def get_RHS_count(self):
        return self.__num_of_RHS
