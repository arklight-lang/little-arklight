# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from asm.parsing.parselets.expressions import LiteralParselet, AssignmentParselet, StaticExpressionParselet, DynamicExpressionParselet
from asm.parsing.parselets.declarations import CircuitDeclarationParselet
from common.token_type import TokenType


class Grammar(object):
    """

    """
    parselets = {
        TokenType.CIRCUIT       : CircuitDeclarationParselet(),
        TokenType.IDENTIFIER    : StaticExpressionParselet(),
        TokenType.PERCENT       : DynamicExpressionParselet(),
        TokenType.EQUAL         : AssignmentParselet(),
        TokenType.CBINARY       : LiteralParselet(),
    }
