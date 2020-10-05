from Scanner import Scanner
from Parser import Parser
while True:
    text = input(">>> ")
    scanner = Scanner(text)
    tokens = scanner.scan()
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast.run())