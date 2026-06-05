from lex import *
from parse import *
import sys

def main():
    print("tiny compiler")

    if len(sys.argv) != 2: # reads arguments from python file call
        sys.exit("Error: Comiler needs source file as argument")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # initliaze the lexer + parse
    lexer = Lexer(source)
    parse = Parser(lexer)

    parser.program()
    print("Parsing completed.")

main()
