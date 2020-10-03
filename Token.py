class TokenType(enum.Enum):
    LEFT_PAREN, RIGHT_PAREN, MINUS, PLUS, SLASH, STAR, EQUAL, IDENTIFIER, NUMBER, STRING = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value