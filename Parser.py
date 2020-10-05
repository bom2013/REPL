from Token import Token, TokenType

var_dict = {}


class Expr():
    factor = None
    mathExpr = None

    def __init__(self, factor=None, mathExpr=None):
        self.factor = factor
        self.mathExpr = mathExpr

    def run(self):
        if factor:
            return self.factor.run()
        return self.mathExpr.run()


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
            return self.value.run()
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
        expr_val = self.expr.run()
        var_dict[self.id] = expr_val
        return expr_val


class Identifier:
    def __init__(self, id):
        self.id = id

    def run(self):
        try:
            return var_dict[self.id]
        except:
            raise Exception(
                f"ERROR: Invalid identifier. No variable with name '{self.id}' was found")


class Literal:
    def __init__(self, value):
        self.value = value

    def run(self):
        return self.value


class Grouping:
    def __init__(self, expr):
        self.expr = expr

    def run(self):
        return self.expr.run()


class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def run(self):
        right_val = self.right.run()
        if self.operator.type == TokenType.MINUS:
            return -right_val
        return right_val


class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def run(self):
        left_val = self.left.run()
        right_val = self.right.run()
        if self.operator.type == TokenType.PLUS:
            return left_val + right_val
        if self.operator.type == TokenType.MINUS:
            return left_val - right_val
        if self.operator.type == TokenType.STAR:
            return left_val * right_val
        if self.operator.type == TokenType.SLASH:
            return left_val / right_val
        if self.operator.type == TokenType.MODULO:
            return left_val % right_val


class Parser():
    '''
    The syntex for this parser:

    expr -> factor | mathExpr
    mathExpr -> add
    add -> mult( ( "-" | "+" ) mult)*
    mult -> unary ( ( "/" | "*" | "%" ) unary )*
    unary -> ("-") unary | primary
    primary -> literal | "(" expr ")"
    factor -> num | id | assignment
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
        '''
        Because it's interactive interpreter, the parser need to work on one line command
        '''
        def is_end():
            return self.index >= len(self.tokens)

        def check(type, offset=0):
            if is_end():
                return False
            return peek(offset).type == type

        def match(*args):
            for type in args:
                if (check(type)):
                    advance()
                    return True
            return False

        def advance():
            if not is_end():
                self.index += 1
            return prev()

        def prev():
            return self.tokens[self.index - 1]

        def peek(offset=0):
            return self.tokens[self.index+offset]

        def remaining_tokens():
            return len(self.tokens) - self.index

        def expression():
            if is_end():
                return None  # it's smart?
            if remaining_tokens() == 1:
                if check(TokenType.NUMBER):
                    return Literal(advance().value)
                if check(TokenType.IDENTIFIER):
                    return Identifier(advance().value)
            if check(TokenType.EQUAL, 1):
                id = advance()
                advance()  # '='
                expr = expression()
                return Assignment(id.value, expr)
            return mathExpr()

        def mathExpr():
            return addition()

        def addition():
            expr = multiplication()
            while match(TokenType.MINUS, TokenType.PLUS):
                operator = prev()
                right = multiplication()
                expr = Binary(expr, operator, right)
            return expr

        def multiplication():
            expr = unary()
            while match(TokenType.SLASH, TokenType.STAR, TokenType.MODULO):
                operator = prev()
                right = unary()
                expr = Binary(expr, operator, right)
            return expr

        def unary():
            if match(TokenType.MINUS):
                operator = prev()
                right = unary()
                return Unary(operator, right)
            return primary()

        def primary():
            if match(TokenType.NUMBER):
                return Literal(prev().value)
            if match(TokenType.LEFT_PAREN):
                expr = expression()
                advance()
                return Grouping(expr)

        return expression()
