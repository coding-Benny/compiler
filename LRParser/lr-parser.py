from input import *
from stack import *
from parsing_table import *
from rule import *
step, action, result = 0, '', ''


class LRParser:
    def __init__(self):
        self.__input: Input = Input()
        self.__stack: Stack = Stack()
        self.__action_table: ActionTable = ActionTable()
        self.__goto_table: GotoTable = GotoTable()
        self.__rules: dict[int, Rule] = {
            1: Rule('E → E + T'),
            2: Rule('E → T'),
            3: Rule('T → T * F'),
            4: Rule('T → F'),
            5: Rule('F → (E)'),
            6: Rule('F → a')
        }

    def build_action_table(self):
        self.__action_table.insert_action(0, Terminal.a.value, 's5')
        self.__action_table.insert_action(0, Terminal.LPAREN.value, 's4')
        self.__action_table.insert_action(1, Terminal.PLUS.value, 's6')
        self.__action_table.insert_action(1, Terminal.DOLLAR.value, 'acc')
        self.__action_table.insert_action(2, Terminal.PLUS.value, 'r2')
        self.__action_table.insert_action(2, Terminal.ASTERISK.value, 's7')
        self.__action_table.insert_action(2, Terminal.RPAREN.value, 'r2')
        self.__action_table.insert_action(2, Terminal.DOLLAR.value, 'r2')
        self.__action_table.insert_action(3, Terminal.PLUS.value, 'r4')
        self.__action_table.insert_action(3, Terminal.ASTERISK.value, 'r4')
        self.__action_table.insert_action(3, Terminal.RPAREN.value, 'r4')
        self.__action_table.insert_action(3, Terminal.DOLLAR.value, 'r4')
        self.__action_table.insert_action(4, Terminal.a.value, 's5')
        self.__action_table.insert_action(4, Terminal.LPAREN.value, 's4')
        self.__action_table.insert_action(5, Terminal.PLUS.value, 'r6')
        self.__action_table.insert_action(5, Terminal.ASTERISK.value, 'r6')
        self.__action_table.insert_action(5, Terminal.RPAREN.value, 'r6')
        self.__action_table.insert_action(5, Terminal.DOLLAR.value, 'r6')
        self.__action_table.insert_action(6, Terminal.a.value, 's5')
        self.__action_table.insert_action(6, Terminal.LPAREN.value, 's4')
        self.__action_table.insert_action(7, Terminal.a.value, 's5')
        self.__action_table.insert_action(7, Terminal.LPAREN.value, 's4')
        self.__action_table.insert_action(8, Terminal.PLUS.value, 's6')
        self.__action_table.insert_action(8, Terminal.RPAREN.value, 's11')
        self.__action_table.insert_action(9, Terminal.PLUS.value, 'r1')
        self.__action_table.insert_action(9, Terminal.ASTERISK.value, 's7')
        self.__action_table.insert_action(9, Terminal.RPAREN.value, 'r1')
        self.__action_table.insert_action(9, Terminal.DOLLAR.value, 'r1')
        self.__action_table.insert_action(10, Terminal.PLUS.value, 'r3')
        self.__action_table.insert_action(10, Terminal.ASTERISK.value, 'r3')
        self.__action_table.insert_action(10, Terminal.RPAREN.value, 'r3')
        self.__action_table.insert_action(10, Terminal.DOLLAR.value, 'r3')
        self.__action_table.insert_action(11, Terminal.PLUS.value, 'r5')
        self.__action_table.insert_action(11, Terminal.ASTERISK.value, 'r5')
        self.__action_table.insert_action(11, Terminal.RPAREN.value, 'r5')
        self.__action_table.insert_action(11, Terminal.DOLLAR.value, 'r5')

    def build_goto_table(self):
        self.__goto_table.insert_goto_state(0, NonTerminal.E.value, 1)
        self.__goto_table.insert_goto_state(0, NonTerminal.T.value, 2)
        self.__goto_table.insert_goto_state(0, NonTerminal.F.value, 3)
        self.__goto_table.insert_goto_state(4, NonTerminal.E.value, 8)
        self.__goto_table.insert_goto_state(4, NonTerminal.T.value, 2)
        self.__goto_table.insert_goto_state(4, NonTerminal.F.value, 3)
        self.__goto_table.insert_goto_state(6, NonTerminal.T.value, 9)
        self.__goto_table.insert_goto_state(6, NonTerminal.F.value, 3)
        self.__goto_table.insert_goto_state(7, NonTerminal.F.value, 10)

    def set_input(self, s: str):
        self.__input.set(s)

    def do_shift(self, current_char: str, num: str):
        global result
        if current_char.isupper():
            current_input = ''.join([key for key, value in terminal_dict.items() if value == current_char])
            self.__stack.push(current_input)
        else:
            self.__stack.push(Terminal[current_char].name)
        self.__stack.push(num)
        self.__input.set(self.__input.increment())
        result += "shift {}\n".format(num)

    def do_reduce(self, num: str):
        global result, step
        rule = self.__rules.get(int(num))
        pop_amount = rule.get_RHS_count() * 2
        for _ in range(pop_amount):
            self.__stack.pop()
        self.__stack.push(rule.get_LHS())

        result += "reduce {}\n".format(num)
        step += 1
        result += "\t{}\t\t{:<18}\t{:>20}\t".format(str(step), ''.join(self.__stack.get_stack()), self.__input.get_input())

        previous_state = int(self.__stack.get_element(-2))
        lhs = NonTerminal[self.__stack.get_element(-1)].value
        state = self.get_next_state_from_goto_table(previous_state, lhs)
        self.__stack.push(state)
        result += "GOTO {}\n".format(state)

    def get_next_state_from_goto_table(self, row: int, col: int):
        state = str(self.__goto_table.get_goto_state(row, col))
        return state

    def perform_parsing(self):
        global result, step, action

        self.__stack.push(str(0))
        while action != 'acc':
            result += "\t{}\t\t{:<18}\t{:>20}\t".format(str(step), ''.join(self.__stack.get_stack()), self.__input.get_input())
            current_char = self.__input.get_input(0)

            try:
                if not current_char.isalpha():
                    current_char = terminal_dict.get(current_char)
                row = self.__stack.get_stack_top()
                if row.isdigit():
                    row = int(row)
                col = Terminal[current_char].value
                action = self.__action_table.get_action_from_action_table(row, col)
                if action == 'acc':
                    result += 'accept\n'
                    return
                do, number = action[0:1], action[1:]
                if do == 's':
                    self.do_shift(current_char, number)
                else:
                    self.do_reduce(number)
                step += 1
            except KeyError:
                result += "\n===================== Error: Undefined input ====================="
                return


def show_parsing_step_header():
    print("┌────────┬─────────────────────┬─────────────────────┬──────────────────┐")
    print("│  Step  │        Stack        │        Input        │      Action      │")
    print("└────────┴─────────────────────┴─────────────────────┴──────────────────┘")


def show_parsing_step():
    print(result)


def main():
    parser = LRParser()
    parser.build_action_table()
    parser.build_goto_table()
    parser.set_input(input('input string = ').replace(' ', '') + '$')
    parser.perform_parsing()

    show_parsing_step_header()
    show_parsing_step()


if __name__ == '__main__':
    main()
