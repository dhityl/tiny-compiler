import sys
from lex import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # called twice to initialize current and peek

    def checkToken(self, kind):
        return kind == self.curToken.kind 

    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error: " + message)

    #Production rules
    # program ::= {statement}
    def program(self):
        print("program")

        while not self.checkToken(TokenType.eof)
            self.statement()

    def statement(self):
        print("statement")
        
        while not self.checkToken(TokenType.eof)
            if self.checkToken() in range(101,200):


