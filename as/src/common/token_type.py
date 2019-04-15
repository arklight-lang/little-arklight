# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from enum import IntEnum

token_types_str = {
    0   : "CIRCUIT",
    1   : "RETURN",
    2   : "LEFT_PAREN",
    3   : "RIGHT_PAREN",
    4   : "LEFT_BRACE",
    5   : "RIGHT_BRACE",
    6   : "LEFT_BRACKET",
    7   : "RIGHT_BRACKET",
    8   : "EQUAL",
    9   : "COLON",
    10  : "SEMI_COLON",
    11  : "COMMA",
    12  : "PERCENT",
    13  : "IDENTIFIER",
    14  : "CBINARY",
    15  : "ERROR",
    16  : "EOF"
}

class TokenType(IntEnum):
    """

    """
    # Keywords
    CIRCUIT         = 0     # circuit
    RETURN          = 1     # return

    # Symbols
    LEFT_PAREN      = 2     # (
    RIGHT_PAREN     = 3     # )
    LEFT_BRACE      = 4     # {
    RIGHT_BRACE     = 5     # }
    LEFT_BRACKET    = 6     # [
    RIGHT_BRACKET   = 7     # ]
    EQUAL           = 8     # =
    COLON           = 9     # :
    SEMI_COLON      = 10    # ;
    COMMA           = 11    # ,
    PERCENT         = 12    # %

    # User defined strings
    IDENTIFIER      = 13    # main, and, not, ...

    # Data structures
    CBINARY         = 14    # 0b

    # Special tokens
    ERROR           = 15    # Error
    EOF             = 16    # End Of File

    def __str__(self):
        return token_types_str[self.value]
