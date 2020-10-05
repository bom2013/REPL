from Token import Token, TokenType


class Scanner():
    def __init__(self, text):
        self.text = text

    def scan(self):
        self.index = 0
        self.tokens = []

        def next():
            '''
            Return next char of code
            *Change index*
            '''
            self.index += 1
            return self.text[self.index - 1]

        def peek(offset=0):
            '''
            Return current char (+ offest)
            *Don't change index*
            '''
            try:
                return self.text[self.index + offset]
            except:
                return ""

        def is_end():
            return self.index >= len(self.text)

        def is_digit(c):
            return c >= '0' and c <= '9'

        def number():
            start = self.index-1
            while is_digit(peek()):
                next()
            # fractional part
            if peek() == '.' and is_digit(peek(1)):
                next()
                while is_digit(peek()):
                    next()
            self.tokens.append(
                Token(TokenType.NUMBER, int(self.text[start:self.index])))

        def identifier():
            start = self.index - 1
            while peek().isalpha():
                next()
            id = self.text[start:self.index]
            self.tokens.append(Token(TokenType.IDENTIFIER, id))

        def get_token():
            c = next()
            if c == "(":
                self.tokens.append(Token(TokenType.LEFT_PAREN, "("))
            elif c == ")":
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ")"))
            elif c == "+":
                self.tokens.append(Token(TokenType.PLUS, "+"))
            elif c == "-":
                self.tokens.append(Token(TokenType.MINUS, "-"))
            elif c == "/":
                self.tokens.append(Token(TokenType.SLASH, "/"))
            elif c == "%":
                self.tokens.append(Token(TokenType.MODULO, "%"))
            elif c == "*":
                self.tokens.append(Token(TokenType.STAR, "*"))
            elif c == "=":
                self.tokens.append(Token(TokenType.EQUAL, "="))
            elif c == " ":
                pass
            elif is_digit(c):
                number()
            elif c.isalpha():
                identifier()
            else:
                raise Exception("Error: Unexpected character")
        while not is_end():
            get_token()
        return self.tokens
