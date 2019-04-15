# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from asm.lexing.exceptions import LexError
from common.token_type import TokenType
from common.token import Token

class Lexer(object):
    """Scans the given string for tokens to be passed to the parser.

    
    """
    source      : str       = ""
    start       : int       = 0
    current     : int       = 0
    line        : int       = 1

    _length     : int       = 0
    _keywords   : dict      = {}
    _gates      : dict      = {}

    def __init__(self, source: str):
        self.source = source
        self._length = len(source)
        self._keywords = {
            "circuit": TokenType.CIRCUIT,
            "return" : TokenType.RETURN,
        }
        self._gates = {
            # "print": TokenType.PRINT,
        }

    def lex(self):
        """Start scanning the source code for lexemes and creating tokens.

        We need to return them tokens somehow to the compiler for processing.
        """
        while True:
            token = self._scanToken()

            # When skipping whitespace and comments, we get None as return value so we skip it here
            if token is None:
                continue

            return token


    def _scanToken(self):
        """Recognize lexemes from the source code, build tokens from the recognized lexemes and return the same."""
        
        # Before scanning the next token, we ignore all whitespace before it
        self._skipWhitespace()

        # Update the start of the new token to be the current location in the source stream
        self.start = self.current

        if self._isAtEnd():
            return self._makeToken(TokenType.EOF)

        # Match one token at a time as we move through the source and return it to the caller
        c = self._advance()
        if c == '(':
            return self._makeToken(TokenType.LEFT_PAREN)

        elif c == ')':
            return self._makeToken(TokenType.RIGHT_PAREN)

        elif c == '{':
            return self._makeToken(TokenType.LEFT_BRACE)

        elif c == '}':
            return self._makeToken(TokenType.RIGHT_BRACE)

        elif c == '[':
            return self._makeToken(TokenType.ERROR, error = "Indexing is not currently supported.")

        elif c == ']':
            return self._makeToken(TokenType.ERROR, error = "Indexing is not currently supported.")

        elif c == '=':
            return self._makeToken(TokenType.EQUAL)

        elif c == ':':
            return self._makeToken(TokenType.COLON)

        elif c == ';':
            return self._makeToken(TokenType.SEMI_COLON)

        elif c == ',':
            return self._makeToken(TokenType.COMMA)

        elif c == '%':
            return self._makeToken(TokenType.PERCENT)

        elif c == '/':
            if self._peek() == '/':
                return self._skipComment()

            else:
                return self._makeToken(TokenType.ERROR, error = "Expected a second slash '/' to indicate a comment.")

        # We got neither one symbol nor two symboles but possibly a number, an identifier or a keyword
        else:
            if c.isalnum():
                if c.isnumeric():
                    return self._scanNumericToken()

                else:
                    return self._scanAlphaToken()

            elif c == '_':
                return self._scanAlphaToken()

            elif c.isspace():
                return self._skipWhitespace()

            else:
                return self._makeToken(TokenType.ERROR, error = "Unexpected token.")

        # If anything else, we return an error
        return self._makeToken(TokenType.ERROR, error = "Unexpected token.")


    def _skipWhitespace(self):
        """Skips any whitespace in the source until a meaningful character is reached."""
        while True:
            c = self._peek()
            if c == ' ' or c == '\r' or c == '\t':
                self._advance()

            elif c == '\n':
                self.line = self.line + 1
                self._advance()

            else:
                return None


    def _skipComment(self):
        """Make sure we match a comment so we can ignore anything after it till the end of the line."""
        while not self._isAtEnd() and self._peek() != '\n':
            self._advance()

        return None


    def _scanNumericToken(self):
        """Scans for a number and returns the corresponding token."""
        while self._isNumeric():
            self._advance()

        # We make sure that the next character is 'b'
        if self._peek() != 'b':
            return self._makeToken(TokenType.ERROR, error = "Expected the letter 'b' after the binary number.")
        else:
            self._advance()

        return self._makeToken(TokenType.CBINARY)


    def _scanAlphaToken(self):
        """Scans for a keyword, instruction or an identifier."""
        while self._isAlpha():
            self._advance()

        alpha = self.source[self.start : self.current]
        try:
            return self._makeToken(self._keywords[alpha])
        except KeyError:
            try:
                return self._makeToken(self._gates[alpha])
            except KeyError:
                return self._makeToken(TokenType.IDENTIFIER)


    def _isNumeric(self):
        """Return true if the current character is a digit."""
        if self._isAtEnd():
            return False

        if self.source[self.current].isnumeric() == False:
            return False

        return True


    def _isAlpha(self):
        """Return true if the current character is a valid keywork or identifier."""
        if self._isAtEnd():
            return False

        if isascii(self.source[self.current]) == False:
            return False

        if (self.source[self.current] >= 'a' and self.source[self.current] <= 'z') or (self.source[self.current] >= 'A' and self.source[self.current] <= 'Z') or (self.source[self.current] >= '0' and self.source[self.current] <= '9') or self.source[self.current] == '_':
            return True

        else:
            return False


    def _advance(self):
        """Consume the current character and returns it."""
        self.current = self.current + 1
        return self.source[self.current - 1]


    def _match(self, expected: str):
        """Returns true if the current character matches the given one, consuming it only if the match is successful."""
        if len(expected) > 1:
            raise LexError("[Lexing Error] Expected a single character in match.")

        if self._isAtEnd():
            return False

        if self.source[self.current] != expected:
            return False

        self.current = self.current + 1
        return True


    def _peek(self):
        """Returns the current character without advancing in the source stream."""
        if self._isAtEnd():
            return None

        return self.source[self.current]


    def _peekNext(self):
        """Returns the character after the current one without advancing in the source stream."""
        if self._isAtEnd():
            return None

        return self.source[self.current + 1]


    def _isAtEnd(self):
        """Returns true if we reached the end of the source, false otherwise."""
        if self.current == self._length:
            return True
        else:
            return False


    def _makeToken(self, token_type: TokenType, error = ""):
        """Given a token type, create a new token corresponding to the current recognized unit."""
        return Token(token_type, self.source[self.start : self.current], self.line, error)


"""Helper function to decide if we got only ASCII characters in our identifiers.

Once we upgrade to Python 3.7, we can use the native str.isascii() function.
"""
isascii = lambda s: len(s) == len(s.encode())
