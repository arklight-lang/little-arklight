# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from asm.parsing.parselets.expressions import LiteralParselet, DynamicExpressionParselet, StaticExpressionParselet, AssignmentParselet
from asm.parsing.parselets.declarations import CircuitDeclarationParselet
from asm.parsing.parselets.statements import ReturnStatementParselet, ExpressionStatementParselet
from common.ast import Program, CircuitDeclaration
from asm.parsing.exceptions import ParseError
from common.token_type import TokenType
from asm.lexing.lexer import Lexer
from common.token import Token


class Parser(object):
    """Invokes the lexer and generates an AST which will be checked for correctness and bytecode generated from it.

    
    """
    lexer           : Lexer     = None
    decls           : dict      = {}
    static_exprs    : dict      = {}
    dynamic_exprs   : dict      = {}
    literal_exprs   : dict      = {}
    assign_exprs    : dict      = {}
    
    _read_tokens    : list      = []

    def __init__(self, lexer: Lexer, parselets: dict):
        self.lexer = lexer

        # Set the grammar
        for token_type, parselet in parselets.items():
            self._register(token_type, parselet)


    def parse(self):
        """
        """
        program = Program()

        while self.peek() != TokenType.EOF:
            decl = self.parseDeclaration()

            # If the current declaration is a circuit declaration and its name is <main>, we set it as the main entry point
            if isinstance(decl, CircuitDeclaration) and decl.token.lexeme == "main":
                program.set_main("main")

            # We don't allow for two declarations to share the same name
            try:
                old_decl = program.get_declaration(decl.token.lexeme)
                raise ParseError("[Parsing Error] There already exists another circuit with the name <" + decl.token.lexeme + "> on line <" + str(old_decl.token.line) + ">.")
            except KeyError:
                pass

            # Add the current declaration to the program list of declarations
            program.add_declaration(decl)

        # We are at the end of the token stream, we consume the EOF token
        self.consume()

        # We return the parse program as an AST
        return program


    def parseDeclaration(self):
        """
        """
        token = self.consume()
        try:
            parselet = self.decls[token.token_type]
            return parselet.parse(self)
        except KeyError:
            raise ParseError("[Parsing Error] Failed to parse declaration <" + token.lexeme + "> found on line <" + str(token.line) + ">.")


    def parseStatement(self):
        """
        """
        # We look two tokens ahead of the current token and if it is a colon, we know we have a labeled statement
        if self._lookAhead(2).token_type == TokenType.COLON:
            return self.parseLabelStatement()

        # We lookahead one token and if we have the return keyword then we have a return statement
        elif self._lookAhead(1).token_type == TokenType.RETURN:
            return self.parseReturnStatement()

        else:
            return self.parseExpressionStatement()


    def parseLabelStatement(self):
        """
        """
        raise ParseError("[Parsing Error] Labeled statements are not currently supported.")


    def parseReturnStatement(self):
        """
        """
        token = self.consume()
        parselet = ReturnStatementParselet()
        return parselet.parse(self, token)


    def parseExpressionStatement(self):
        """
        """
        parselet = ExpressionStatementParselet()
        return parselet.parse(self)


    def parseExpression(self):
        """
        """
        current_token = self.consume()

        # We begin by checking if we have a static expression
        lval = None
        if current_token.token_type in self.static_exprs:
            static_parselet = self.static_exprs[current_token.token_type]
            lval = static_parselet.parse(self, current_token)

        # If the current token points to a dynamic expression, we parse it as such
        elif current_token.token_type in self.dynamic_exprs:
            dynamic_parselet = self.dynamic_exprs[current_token.token_type]
            lval = dynamic_parselet.parse(self, current_token)

        # If on the other hand we have a literal expression, we do the same
        elif current_token.token_type in self.literal_exprs:
            literal_parselet = self.literal_exprs[current_token.token_type]
            lval = literal_parselet.parse(self, current_token)

        # Anything else is a parsing error
        else:
            raise ParseError("[Parsing Error] Failed to parse expression <" + current_token.lexeme + "> found on line <" + str(current_token.line) + ">.")

        # Now we check if we have an assignment after afterwards
        assignment_token = self._lookAhead(1)
        try:
            assignment_parselet = self.assign_exprs[assignment_token.token_type]
            self.consume()
            return assignment_parselet.parse(self, lval, current_token)
        except KeyError:
            return lval

    
    def _register(self, token_type: TokenType, parselet):
        """
        """
        # Circuit declarations are the only kinds of declarations we have right now
        if isinstance(parselet, CircuitDeclarationParselet):
            self.decls[token_type] = parselet

        # Expressions that begin with a percent sign
        elif isinstance(parselet, DynamicExpressionParselet):
            self.dynamic_exprs[token_type] = parselet

        # Expressions that begin with an identifier
        elif isinstance(parselet, StaticExpressionParselet):
            self.static_exprs[token_type] = parselet

        # Assignment expressions are the only infix operators we have
        elif isinstance(parselet, AssignmentParselet):
            self.assign_exprs[token_type] = parselet

        # Literal expressions
        elif isinstance(parselet, LiteralParselet):
            self.literal_exprs[token_type] = parselet

        else:
            raise ParseError("[Assembler Error] Failed to register parselet of unknown type: < " + str(parselet.__class__.__name__) + ">.")


    def consume(self, expected: TokenType = None):
        """
        """
        if expected is not None:
            token = self._lookAhead(1)
            if expected != token.token_type:
                raise ParseError("[Parsing Error] Expected token <" + str(expected) + "> but found <" + str(token.token_type) + "> on line <" + str(token.line) + ">.")

        self._lookAhead(1)
        read_token = self._read_tokens[0]
        del self._read_tokens[0]
        return read_token


    def match(self, expected: TokenType):
        """
        """
        token = self._lookAhead(1)
        if token.token_type != expected:
            return False

        self.consume()
        return True


    def peek(self):
        """
        """
        return self._lookAhead(1).token_type


    def _lookAhead(self, distance: int):
        """
        """
        while distance > len(self._read_tokens):
            # token = self.lexer.lex()
            # print("{:<3d} {}".format(token.token_type.value, token.lexeme))
            self._read_tokens.append(self.lexer.lex())

        return self._read_tokens[distance - 1]
