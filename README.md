# REPL - Simpler Interactive interpreter
This program is a simle Interactive interpreter writen in Python  
## how to use?
1. Download the repo
2. Run repl.py
3. Have fun :)
## How it's work?
1. The main file(repl.py) read command
2. The scanner(Scanner.py) tokenize the command
3. The parser(Parser.py) parse the token list and create AST(Abstract Syntex Tree)
4. The repl run the AST