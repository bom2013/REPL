'''
This file needed only for the codewars kata
'''

from Scanner import Scanner
from Parser import Parser

class Interpreter:
    def input(self, code):
        scanner = Scanner(code)
        tokens = scanner.scan()
        parser = Parser(tokens)
        ast = parser.parse()
        return ast.run()