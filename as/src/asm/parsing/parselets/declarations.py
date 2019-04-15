# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from abc import ABC, abstractmethod

from common.ast import CircuitDeclaration
from common.token_type import TokenType
from common.token import Token


class CircuitDeclarationParselet(object):
    """Parses a circuit declaration."""
    def parse(self, parser):
        # We build the circuit declaration by first consuming the circuit name
        decl = CircuitDeclaration(parser.consume(TokenType.IDENTIFIER))

        # We parse parameters
        parser.consume(TokenType.LEFT_PAREN)
        while True:
            # If the left parenthesis is immediately followed by a right parenthesis, we exit early
            if parser.peek() == TokenType.RIGHT_PAREN:
                break

            # Parse each expression and pass it as parameter to the circuit expression
            arg = parser.parseExpression()
            decl.add_parameter(arg)

            # The moment we run out of commas, we quit
            if parser.match(TokenType.COMMA) == False:
                break

        # We expect a closing right token
        parser.consume(TokenType.RIGHT_PAREN)

        # We parse the circuit body
        parser.consume(TokenType.LEFT_BRACE)
        while True:
            # We match a closing brace, we terminate the loop
            if parser.match(TokenType.RIGHT_BRACE):
                break

            # Get statements that make up the body of the circuit
            stmt = parser.parseStatement()
            decl.add_statement(stmt)

        # We are done, we return the parsed declaration
        return decl
