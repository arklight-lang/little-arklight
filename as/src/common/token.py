# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from common.token_type import TokenType

class Token(object):
    """

    """
    token_type  : TokenType     = None
    lexeme      : str           = ""
    line        : int           = 0
    error       : str           = ""

    def __init__(self, token_type: TokenType, lexeme: str, line: int, error: str):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.error = error

    def __eq__(self, other):
        return self.token_type == other.token_type and self.lexeme == other.lexeme

    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        return "{2} : {0}[{1}]".format(self.lexeme, self.token_type, self.line)

    __str__ = __repr__
