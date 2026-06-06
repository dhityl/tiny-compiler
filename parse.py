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

    # Production rules (maps grammar.txt)
    # program ::= {statement}
    def program(self):
        print("program")

        while not self.checkToken(TokenType.eof):
            self.statement()

    # statement ::= [keywords}
    def statement(self):
        print("statement; ", end="")

        if self.checkToken(TokenType.print):
            print("print")
            self.nextToken()

            if self.checkToken(TokenType.string):
                self.nextToken()
            else:
                self.expression()

        elif self.checkToken(TokenType.when):
            print("when")
            self.nextToken()
            self.comparison()

            self.match(TokenType.then)
            self.nl()

            while not self.checkToken(TokenType.endwhen):
                self.statement()

            self.match(TokenType.endwhen)

        elif self.checkToken(TokenType.loop):
            print("loop")
            self.nextToken()
            self.expression()

            self.match(TokenType.repeat)
            self.nl()

            while not self.checkToken(TokenType.endloop):
                self.statement()

            self.match(TokenType.endwhile)

        elif self.checkToken(TokenType.label):
            print("label")
            self.nextToken()
            self.match(TokenType.identifier)

        elif self.checkToken(TokenType.goto):
            print("goto")
            self.nextToken()
            self.match(TokenType.identifier)

        elif self.checkToken(TokenType.let):
            print("let")
            self.nextToken()
            self.match(TokenType.identifier)
            self.match(TokenType.eq)
            self.expression()

        elif self.checkToken(TokenType.input):
            print("input")
            self.nextToken()
            self.match(TokenType.identifier)

        else: #error!
            self.abort("Invalid statement at " + self.curToken.text + "(" + self.curToken.kind.name + ")")

        self.nl()


    # nl ::= '\n'+
    def nl(self):
        print("newline")

        self.match(TokenType.newline)

        while self.checkToken(TokenType.newline):
            self.nextToken()

