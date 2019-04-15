# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from common.ast import ReturnStatement, ExpressionStatement
from common.token_type import TokenType
from common.token import Token


class ReturnStatementParselet(object):
    """Parses a return statement within a circuit."""
    def parse(self, parser, token: Token):
        # We parse the expression to return
        expr = parser.parseExpression()

        # We consume the semicolon that terminates an expression statement
        parser.consume(TokenType.SEMI_COLON)

        return ReturnStatement(token, expr)


class ExpressionStatementParselet(object):
    """Parses a circuit declaration."""
    def parse(self, parser):
        # We parse the expression proper
        expr = parser.parseExpression()

        # We consume the semicolon that terminates an expression statement
        parser.consume(TokenType.SEMI_COLON)

        return ExpressionStatement(expr)
