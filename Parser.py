from Token import Token, TokenType

var_dict = {}


class Expr():
    factor = None
    opr_expr = None

    def __init__(self, factor=None, opr_expr=None):
        self.factor = factor
        self.opr_expr = opr_expr

    def run(self):
        if factor:
            return self.factor.run()
        return self.opr_expr.run()


class Opr():
    opr = None
    left = None
    right = None

    def __init__(self, opr, left, right):
        self.opr = opr
        self.left = left
        self.right = right

    def run(self):
        left_val = self.left.run()
        right_val = self.right.run()
        if opr == "+":
            return left_val + right_val
        if opr == "-":
            return left_val - right_val
        if opr == "*":
            return left_val * right_val
        if opr == "/":
            return left_val / right_val
        if opr == "%":
            return left_val % right_val
        raise Exception("Error: Missing / unidentified operator")


class Factor():
    value = None

    def __init__(self, value):
        self.value = value

    def run(self):
        if isinstance(self.value, float):
            return self.value
        if isinstance(self.value, Assignment):
            return self.value.run()
        if isinstance(self.value, Expr):
            return Expr.run()
        try:
            return var_dict[self.value]
        except:
            return Exception(f"ERROR: Invalid identifier. No variable with name '{self.value}' was found")


class Assignment():
    id = None
    expr = None

    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def run(self):
        expr_val = expr.run()
        var_dict[id] = expr_val
        return expr_val


class Parser():
    '''
    The syntex for this parser:

    expr -> factor | expr opr expr
    factor -> num | id | assignment | '(' expr ')'
    assignment -> id '=' expr
    opr -> '+' | '-' | '*' | '/' | '%'
    id -> letter | '_' { id_char }
    id_char -> '_' | letter | digit
    num -> { digit } [ '.' digit { digit } ]
    letter -> 'a' | 'b' | ... | 'y' | 'z' | 'A' | 'B' | ... | 'Y' | 'Z'
    digit -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    '''

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        def is_operator(op):
            return op in "+-/%*"

        def is_have_opr_in_code(offset=0):
            return len([i for i in self.tokens[offset:] if is_operator(i.value)]) > 0

        def match(*args, offset=0):
            for type in args:
                if (check(type, offset)):
                    advance(offset)
                    return True
            return False

        def check(type, offset=0):
            if is_end(offset):
                return False
            return peek(offset).type == type

        def advance(offset=0):
            if not is_end():
                self.index += 1 + offset
            return prev(-offset)

        def prev(offset=0):
            return self.tokens[self.index - 1 + offset]

        def peek(offset=0):
            return self.tokens[self.index + offset]

        def is_end():
            return self.index >= len(self.tokens)

        def expression(offset=0):
            if check(TokenType.IDENTIFIER):
                if check(TokenType.EQUAL, 1):
                    return assignment()
                left = expr()

        expression()
