import sys
from lex import *
from emit import *


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  # called twice to initialize current and peek

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
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        # skip newlines
        while self.checkToken(TokenType.newline):
            self.nextToken()

        # parse all statements
        while not self.checkToken(TokenType.eof):
            self.statement()

        # wrap things up w/ emitter
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Undeclared Label: "+ label)

    # statement ::= [keywords}
    def statement(self):
        if self.checkToken(TokenType.print):
            self.nextToken()

            if self.checkToken(TokenType.string):
                # simple sting, so just print it
                self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
                self.nextToken()
            else:
                # expect an expression and print result as float
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

        # "when" comparison "then" nl {statement} "endwhen" nl
        elif self.checkToken(TokenType.when):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.then)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokenType.endwhen):
                self.statement()

            self.match(TokenType.endwhen)
            self.emitter.emitLine("}")
        
        # "loop" comparison "repeat" nl {statement} "endloop" nl
        elif self.checkToken(TokenType.loop):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.repeat)
            self.nl()
            self.emitter.emitLine("){")

            while not self.checkToken(TokenType.endloop):
                self.statement()

            self.match(TokenType.endloop)
            self.emitter.emitLine("}")

        # "label" identifier nl
        elif self.checkToken(TokenType.label):
            self.nextToken()

            # make surethis label doesn't already exit
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emitLine(self.curToken.text + ":")
            self.match(TokenType.identifier)

        # "goto" identifier nl
        elif self.checkToken(TokenType.goto):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emitLine("goto" + self.curToken.text + ";")
            self.match(TokenType.identifier)

        # "let" identifier "=" expression nl
        elif self.checkToken(TokenType.let):
            self.nextToken()

            # if identifier doesnt already exist, declare it 
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokenType.identifier)
            self.match(TokenType.eq)

            self.expression()
            self.emitter.emitLine(";")

        # "input" identifier nl
        elif self.checkToken(TokenType.input):
            self.nextToken()

            # if variable doesnt already exist, declare it
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            # emit scanf after valicating input, if invalid, set variable to 0 and clear input
            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
            self.emitter.emitLine(self.curToken.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.identifier)

        else:  # error!
            self.abort(
                "Invalid statement at "
                + self.curToken.text
                + "("
                + self.curToken.kind.name
                + ")"
            )

        self.nl()

    # comparison ::= (("==" | "!=" | ">" | "<" | "<=" | ">=" ) expression)+
    def comparison(self):
        self.expression()
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()

        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()

    def isComparisonOperator(self):
        # return true if operator lt, lteq, gt, gteq, eqeq, noteq
        return (self.checkToken(TokenType.lt)
        or self.checkToken(TokenType.lteq)
        or self.checkToken(TokenType.gt)
        or self.checkToken(TokenType.gteq)
        or self.checkToken(TokenType.gt)
        or self.checkToken(TokenType.eqeq)
        or self.checkToken(TokenType.noteq))

    # expression ::= term {( "-" | "+") term}
    def expression(self):
        self.term()
        while self.checkToken(TokenType.plus) or self.checkToken(TokenType.minus):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()

    def term(self):
        self.unary()
        while self.checkToken(TokenType.asterisk) or self.checkToken(TokenType.slash):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()

    def unary(self):
        if self.checkToken(TokenType.plus) or self.checkToken(TokenType.minus):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        self.primary()

    def primary(self):
        if self.checkToken(TokenType.number):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.identifier):
            # ensure variable exists
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable without assignment: " + self.curToken.text)

            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text)

    # nl ::= '\n'+
    def nl(self):
        self.match(TokenType.newline)

        while self.checkToken(TokenType.newline):
            self.nextToken()

