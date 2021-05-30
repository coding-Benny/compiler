from input import *
from stack import *
from parsing_table import *
from rule import *

result = ''


class LRParser:
    def __init__(self):
        self.input: Input = Input()
        self.stack: Stack = Stack()
        self.action_table: ActionTable = ActionTable()
        self.goto_table: GotoTable = GotoTable()
        self.rules: dict[int, Rule] = {
            1: Rule('E → E + T'),
            2: Rule('E → T'),
            3: Rule('T → T * F'),
            4: Rule('T → F'),
            5: Rule('F → (E)'),
            6: Rule('F → a')
        }

    def build_action_table(self):
        self.action_table.insert_action(0, Terminal.a.value, 's5')
        self.action_table.insert_action(0, Terminal.LPAREN.value, 's4')
        self.action_table.insert_action(1, Terminal.PLUS.value, 's6')
        self.action_table.insert_action(1, Terminal.DOLLAR.value, 'acc')
        self.action_table.insert_action(2, Terminal.PLUS.value, 'r2')
        self.action_table.insert_action(2, Terminal.ASTERISK.value, 's7')
        self.action_table.insert_action(2, Terminal.RPAREN.value, 'r2')
        self.action_table.insert_action(2, Terminal.DOLLAR.value, 'r2')
        self.action_table.insert_action(3, Terminal.PLUS.value, 'r4')
        self.action_table.insert_action(3, Terminal.ASTERISK.value, 'r4')
        self.action_table.insert_action(3, Terminal.RPAREN.value, 'r4')
        self.action_table.insert_action(3, Terminal.DOLLAR.value, 'r4')
        self.action_table.insert_action(4, Terminal.a.value, 's5')
        self.action_table.insert_action(4, Terminal.LPAREN.value, 's4')
        self.action_table.insert_action(5, Terminal.PLUS.value, 'r6')
        self.action_table.insert_action(5, Terminal.ASTERISK.value, 'r6')
        self.action_table.insert_action(5, Terminal.RPAREN.value, 'r6')
        self.action_table.insert_action(5, Terminal.DOLLAR.value, 'r6')
        self.action_table.insert_action(6, Terminal.a.value, 's5')
        self.action_table.insert_action(6, Terminal.LPAREN.value, 's4')
        self.action_table.insert_action(7, Terminal.a.value, 's5')
        self.action_table.insert_action(7, Terminal.LPAREN.value, 's4')
        self.action_table.insert_action(8, Terminal.PLUS.value, 's6')
        self.action_table.insert_action(8, Terminal.RPAREN.value, 's11')
        self.action_table.insert_action(9, Terminal.PLUS.value, 'r1')
        self.action_table.insert_action(9, Terminal.ASTERISK.value, 's7')
        self.action_table.insert_action(9, Terminal.RPAREN.value, 'r1')
        self.action_table.insert_action(9, Terminal.DOLLAR.value, 'r1')
        self.action_table.insert_action(10, Terminal.PLUS.value, 'r3')
        self.action_table.insert_action(10, Terminal.ASTERISK.value, 'r3')
        self.action_table.insert_action(10, Terminal.RPAREN.value, 'r3')
        self.action_table.insert_action(10, Terminal.DOLLAR.value, 'r3')
        self.action_table.insert_action(11, Terminal.PLUS.value, 'r5')
        self.action_table.insert_action(11, Terminal.ASTERISK.value, 'r5')
        self.action_table.insert_action(11, Terminal.RPAREN.value, 'r5')
        self.action_table.insert_action(11, Terminal.DOLLAR.value, 'r5')

    def build_goto_table(self):
        self.goto_table.insert_goto_state(0, NonTerminal.E.value, 1)
        self.goto_table.insert_goto_state(0, NonTerminal.T.value, 2)
        self.goto_table.insert_goto_state(0, NonTerminal.F.value, 3)
        self.goto_table.insert_goto_state(4, NonTerminal.E.value, 8)
        self.goto_table.insert_goto_state(4, NonTerminal.T.value, 2)
        self.goto_table.insert_goto_state(4, NonTerminal.F.value, 3)
        self.goto_table.insert_goto_state(6, NonTerminal.T.value, 9)
        self.goto_table.insert_goto_state(6, NonTerminal.F.value, 3)
        self.goto_table.insert_goto_state(7, NonTerminal.F.value, 10)

    def set_input(self, s: str):
        self.input.set(s)

    def do_shift(self, current_char: str, num: str):
        if current_char.isupper():
            current_input = ''.join([key for key, value in terminal_dict.items() if value == current_char])
            self.stack.push(current_input)
        else:
            self.stack.push(Terminal[current_char].name)
        self.stack.push(num)
        self.input.set(self.input.increment())

    def do_reduce(self, num: str):
        rule = self.rules.get(int(num))
        pop_amount = rule.get_RHS_count() * 2
        for _ in range(pop_amount):
            self.stack.pop()
        self.stack.push(rule.get_LHS())

    def get_next_state_from_goto_table(self, row: int, col: int):
        state = str(self.goto_table.get_goto_state(row, col))
        self.stack.push(state)
        return state

    def perform_parsing(self):
        global result
        step, action = 0, ''
        self.stack.push(str(0))
        while action != 'acc':
            result += "\t{}\t\t{:<18}\t{:>20}\t".format(str(step), ''.join(self.stack.get_stack()), self.input.get_input())
            current_char = self.input.get_input(0)

            try:
                if is_terminal(self.stack.get_stack_top()):
                    if not current_char.isalpha():
                        current_char = terminal_dict.get(current_char)
                    row = self.stack.get_stack_top()
                    if row.isdigit():
                        row = int(row)
                    col = Terminal[current_char].value
                    action = self.action_table.get_action_from_action_table(row, col)
                    if action == 'acc':
                        result += 'accept\n'
                        return
                    do, number = action[0:1], action[1:]
                    if do == 's':
                        self.do_shift(current_char, number)
                    else:
                        self.do_reduce(number)
                    result += "{} {}\n".format(action_dict.get(do), number)
                else:
                    previous_state = int(self.stack.get_element(-2))
                    lhs = NonTerminal[self.stack.get_element(-1)].value
                    state = self.get_next_state_from_goto_table(previous_state, lhs)
                    result += "GOTO {}\n".format(state)
                step += 1
            except KeyError:
                result += "\n===================== Error: Undefined input ====================="
                return


def is_terminal(c: str):
    return not c.isupper()


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
