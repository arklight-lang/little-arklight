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
from common.token import Token
from asm.lexer import Lexer

class Preprocessor(object):
    """Performs an in-place circuit replacement on their call site and includes files by copy-pasting them.

    The preprocessor is called to do shit the parser doesn't want to deal with.

    Attributes:
        source(str): the main source file from which to generate the executable bytecode.

    TODO:
        - Give a better but equally lazy description of what the preprocessor actually does.
    """
    source: str     = ""

    def __init__(self, source: str):
        self.source = source


    def process(self):
        pass
