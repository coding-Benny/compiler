from input import *
from stack import *
from parsing_table import *

result = ''


class PDParser:
    def __init__(self):
        self.input: Input = Input()
        self.stack: Stack = Stack()
        self.parsingTable: ParsingTable = ParsingTable()

    def build_parsing_table(self):
        self.parsingTable.insert_rule(Rule(1, 'S → aS'))
        self.parsingTable.insert_rule(Rule(2, 'S → bA'))
        self.parsingTable.insert_rule(Rule(3, 'A → d'))
        self.parsingTable.insert_rule(Rule(4, 'A → ccA'))

    def perform_parsing(self):
        global result
        step, action, parse, str_parse = 1, 'expand', [], ''
        self.stack.push('S')
        while not bool(self.stack.is_empty() and self.input.is_empty()):
            result += "    {:^2}      {:<12} {:>10}     ".format(step, ''.join(self.stack.get_stack()),
                                                                 self.input.get_input())
            if is_non_terminal(self.stack.get_stack_top()):
                row = self.stack.get_stack_top()
                col = self.input.get_input(0)
                try:
                    rule = self.parsingTable.get_rule(row, col)
                    self.stack.expand(rule.get_RHS())
                    action = 'expand'
                    parse.append(str(rule.get_id()))
                    str_parse = ''.join(parse)
                    result += "{} {:<10} {}\n".format(action, rule.get_id(), str_parse)
                except KeyError:
                    result += "\n===================== Error: Undefined grammar  ====================="
                    return
            else:
                if self.stack.get_stack_top() == self.input.get_input(0):
                    self.stack.pop()
                    self.input.set(self.input.increment())
                    action = 'pop & advance'
                    result += "{:<14}    {}\n".format(action, str_parse)
            step += 1
        action = 'accept'
        result += "    {:^2}      {:<12} {:>10}     {:<14}    {}\n".format(step, ''.join(self.stack.get_stack()),
                                                                           self.input.get_input(), action, str_parse)

    def set_input(self, s: str):
        self.input.set(s)

    def is_stack_empty(self):
        return self.stack.is_empty()

    def is_input_empty(self):
        return self.input.is_empty()


def is_non_terminal(c: str):
    return c.isupper()


def show_parsing_step_header():
    print("┌────────┬─────────────┬─────────────┬──────────────────┬───────────┐")
    print("│  Step  │    Stack    │    Input    │      Action      │   Parse   │")
    print("└────────┴─────────────┴─────────────┴──────────────────┴───────────┘")


def show_parsing_step():
    print(result)


def main():
    parser = PDParser()
    parser.build_parsing_table()
    parser.set_input(input('input string = ') + '$')
    parser.perform_parsing()

    show_parsing_step_header()
    show_parsing_step()


if __name__ == '__main__':
    main()
