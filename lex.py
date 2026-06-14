from sys import exit
from enum import Enum


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.curChar = ""
        self.curPos = -1
        self.nextChar()

    # process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.curPos + 1]

    # invalid token, print error and exit
    def abort(self, message):
        exit("Lexing error: " + message)

    # skip whitespaces except newlines
    def skipWhitespace(self):
        if self.curChar == " " or self.curChar == "\t" or self.curChar == "\r":
            self.nextChar()

    # Skip comments in the code
    def skipComment(self):
        if self.curChar == "~":
            while self.curChar != "\n":
                self.nextChar()

    #  return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # operators
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.plus)

        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.minus)

        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.astersisk)

        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.slash)

        elif self.curChar == "=":
            # check if the toekn is = or ==
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.eqeq)
            else:
                token = Token(self.curChar, TokenType.eq)

        elif self.curChar == "<":
            # check if the token is < or <=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.lteq)
            else:
                token = Token(self.curChar, TokenType.lt)

        elif self.curChar == ">":
            # check if the token is > or >=
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.gteq)
            else:
                token = Token(self.curChar, TokenType.gt)

        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.noteq)
            else:
                self.abort("Expected !=, got !" + self.peek())

        # numbers
        elif self.curChar.isdigit():
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == ".":
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number:" + self.curChar)

                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            token = Token(tokText, TokenType.number)

        # strings
        elif self.curChar == '"':
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '"':
                # not allowing special characters in a string
                if self.curChar in ["\r", "\n", "\t", "\\", "%"]:
                    self.abort("Invalid character in string:" + self.curChar)
                self.nextChar()
            tokText = self.source[startPos : self.curPos]
            token = Token(tokText, TokenType.string)

        # keywords or identifiers
        elif self.curChar.isalpha():
            # get all consecutive alpha-numeric characters
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            tokText = self.source[startPos : self.curPos + 1]
            keyword = Token.checkKeyword(tokText.lower())
            if keyword == None:  # identifier
                token = Token(tokText, TokenType.identifier)
            else:  # keyword
                token = Token(tokText, keyword)

        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.newline)

        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.eof)

        else:
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def checkKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class TokenType(Enum):
    eof = -1
    newline = 0
    number = 1
    string = 2
    identifier = 3

    # Keywords
    label = 101
    goto = 102
    print = 103
    input = 104
    let = 105
    when = 106  # can't use if cause python keyword
    then = 107
    endwhen = 108
    loop = 109
    repeat = 110
    endloop = 111

    # Operators
    eq = 201
    plus = 202
    minus = 203
    astersisk = 204
    slash = 205
    eqeq = 206
    noteq = 207
    lt = 208
    lteq = 209
    gt = 210
    gteq = 211
