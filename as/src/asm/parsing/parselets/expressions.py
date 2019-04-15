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
from common.ast import (
    Expression,
    GateExpression,
    CircuitExpression,
    LiteralExpression,
    RegisterExpression,
    ParameterExpression,
    AssignmentExpression,
)


class StaticExpressionParselet(object):
    """Abstract class for """
    def parse(self, parser, token: Token):
        """Parses expressions that will not be rewritten/expanded but are part of the VM."""
        parselet = None

        # We decide if we have a register expression or a gate application expression
        if parser.peek() == TokenType.LEFT_PAREN:
            parselet = GateParselet()
            return parselet.parse(parser, token)

        else:
            parselet = RegisterParselet()
            return parselet.parse(parser, token)


class DynamicExpressionParselet(object):
    def parse(self, parser, token: Token):
        """Parses expressions that will be rewritten/expanded as they are not part of the VM."""
        parselet = None

        # We received a percent sign, we have either a parameter expression or a circuit invocation expression
        identifier = parser.consume(TokenType.IDENTIFIER)
        if parser.peek() == TokenType.LEFT_PAREN:
            parselet = CircuitParselet()
            return parselet.parse(parser, identifier)

        else:
            parselet = ParameterParselet()
            return parselet.parse(parser, identifier)


class AssignmentParselet(object):
    def parse(self, parser, lval: Expression, token: Token):
        """Parses an assignment expression."""
        rval = parser.parseExpression()
        return AssignmentExpression(token, lval, rval)


class CircuitParselet(DynamicExpressionParselet):
    def parse(self, parser, token: Token):
        """Parses a circuit application expression."""
        circuit_expr = CircuitExpression(token)

        parser.consume(TokenType.LEFT_PAREN)
        while True:
            # If the left parenthesis is immediately followed by a right parenthesis, we exit early
            if parser.peek() == TokenType.RIGHT_PAREN:
                break

            # Parse each expression and pass it as argument to the circuit expression
            arg = parser.parseExpression()
            circuit_expr.add_argument(arg)

            # The moment we run out of commas, we quit
            if parser.match(TokenType.COMMA) == False:
                break
        # We expect a closing right token
        parser.consume(TokenType.RIGHT_PAREN)

        return circuit_expr


class GateParselet(StaticExpressionParselet):
    def parse(self, parser, token: Token):
        """Parses a gate application expression."""
        gate_expr = GateExpression(token)

        parser.consume(TokenType.LEFT_PAREN)
        while True:
            # If the left parenthesis is immediately followed by a right parenthesis, we exit early
            if parser.peek() == TokenType.RIGHT_PAREN:
                break

            # Parse each expression and pass it as argument to the gate expression
            arg = parser.parseExpression()
            gate_expr.add_argument(arg)

            # The moment we run out of commas, we quit
            if parser.match(TokenType.COMMA) == False:
                break;
        # We expect a closing right token
        parser.consume(TokenType.RIGHT_PAREN)

        return gate_expr


class ParameterParselet(DynamicExpressionParselet):
    def parse(self, parser, token: Token):
        """Parses a parameter use expression."""
        return ParameterExpression(token)


class RegisterParselet(StaticExpressionParselet):
    def parse(self, parser, token: Token):
        """Parses a register use expression."""
        return RegisterExpression(token)


class LiteralParselet(object):
    def parse(self, parser, token: Token):
        """Parses a literal expression."""
        return LiteralExpression(token)
