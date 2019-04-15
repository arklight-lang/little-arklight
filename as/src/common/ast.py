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

from common.token import Token


class Program(object):
    """

    """
    decls   : dict          = {}
    main    : str           = ""

    def __init__(self):
        """
        """
        self.decls = {}
        self.main = ""


    def add_declaration(self, decl):
        """
        """
        self.decls[decl.token.lexeme] = decl


    def get_declaration(self, name: str, arity: int = None):
        """
        """
        decl = self.decls[name]
        if arity is not None and len(decl.params) != arity:
            raise KeyError("Declaration with name <" + name + "> with arity <" + str(arity) + "> not found.")
        
        return decl


    def has_declaration(self, name: str):
        """
        """
        return name in self.decls


    def set_main(self, name: str):
        """
        """
        self.main = name


    def get_main(self):
        """
        """
        return self.decls["main"]

    def clean(self):
        """
        """
        for name in list(self.decls.keys()):
            if name != "main":
                del self.decls[name]


    def __repr__(self):
        rep = ""
        for name, decl in self.decls.items():
            rep = rep + "{0!s}\n".format(decl)
        return rep

    __str__ = __repr__


class CircuitDeclaration(object):
    """

    """
    token   : Token             = None
    params  : list              = []
    stmts                       = None

    def __init__(self, token: Token):
        """
        """
        self.token = token
        self.params = []
        self.stmts = CircuitStatements()


    def add_parameter(self, parameter):
        """
        """
        self.params.append(parameter)


    def add_statement(self, statement):
        """
        """
        self.stmts.append(statement)


    def __repr__(self):
        rep = "circuit {0!s}(".format(self.token.lexeme)

        # Print the circuit parameters
        for index, param in enumerate(self.params):
            rep = rep + "{0!s}".format(param)
            if index != len(self.params) - 1:
                rep = rep + ", "
        rep = rep + ") {\n"

        # Print the circuit body
        for stmt in self.stmts:
            rep = rep + "   {0!s}".format(stmt)
        rep = rep + "}\n"

        return rep

    __str__ = __repr__


class Statement(ABC):
    """

    """
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class LabeledStatement(Statement):
    """

    """
    token   : Token         = None

    def __init__(self, token: Token):
        """
        """
        self.token = token


    def __repr__(self):
        return "{0!s}:\n".format(self.token.lexeme)

    __str__ = __repr__


class ReturnStatement(Statement):
    """

    """
    token   : Token         = None
    expr                    = None

    def __init__(self, token, expr):
        """
        """
        self.token = token
        self.expr = expr


    def __repr__(self):
        return "return {0!s};\n".format(self.expr)

    __str__ = __repr__


class ExpressionStatement(Statement):
    """

    """
    token   : Token         = None
    expr                    = None

    def __init__(self, expr):
        """
        """
        self.token = expr.token
        self.expr = expr


    def __repr__(self):
        return "{0!s};\n".format(self.expr)

    __str__ = __repr__


class Expression(ABC):
    """

    """
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class AssignmentExpression(Expression):
    """

    """
    token   : Token         = None
    lval    : Expression    = None
    rval    : Expression    = None

    def __init__(self, token: Token, lval, rval):
        """
        """
        self.token = token
        self.lval = lval
        self.rval = rval


    def __eq__(self, other):
        return self.token == other.token


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        return "{0!s} = {1!s}".format(self.lval, self.rval)

    __str__ = __repr__


class CircuitExpression(Expression):
    """

    """
    token   : Token         = None
    args    : list          = []

    def __init__(self, token: Token):
        """
        """
        self.token = token
        self.args = []


    def add_argument(self, arg):
        """
        """
        if isinstance(arg, Expression) == False:
            raise ValueError("The given argument to a circuit expander must an expression.")

        self.args.append(arg)


    def __eq__(self, other):
        return self.token == other.token and self.args == other.args


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        """
        """
        rep = "%{0!s}".format(self.token.lexeme)
        rep = rep + "("
        for index, arg in enumerate(self.args):
            rep = rep + "{0!s}".format(arg)
            if index != len(self.args) - 1:
                rep = rep + ", "
        rep = rep + ")"

        return rep

    __str__ = __repr__


class GateExpression(Expression):
    """

    """
    token   : Token         = None
    args    : list          = []

    def __init__(self, token: Token):
        """
        """
        self.token = token
        self.args = []


    def add_argument(self, arg):
        """
        """
        if isinstance(arg, Expression) == False:
            raise ValueError("The given argument to a gate must an expression.")

        self.args.append(arg)


    def __eq__(self, other):
        return self.token == other.token and self.args == other.args


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        """
        """
        rep = "{0!s}".format(self.token.lexeme)
        rep = rep + "("
        for index, arg in enumerate(self.args):
            rep = rep + "{0!s}".format(arg)
            if index != len(self.args) - 1:
                rep = rep + ", "
        rep = rep + ")"

        return rep

    __str__ = __repr__


class ParameterExpression(Expression):
    """

    """
    token   : Token         = None

    def __init__(self, token: Token):
        """
        """
        self.token = token


    def __eq__(self, other):
        return self.token == other.token


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        """
        """
        return "%{0!s}".format(self.token.lexeme)

    __str__ = __repr__


class RegisterExpression(Expression):
    """

    """
    token   : Token         = None

    def __init__(self, token: Token):
        """
        """
        self.token = token


    def __eq__(self, other):
        return self.token == other.token


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        """
        """
        return "{0!s}".format(self.token.lexeme)

    __str__ = __repr__



class LiteralExpression(Expression):
    """

    """
    token   : Token         = None

    def __init__(self, token: Token):
        """
        """
        self.token = token


    def __eq__(self, other):
        return self.token == other.token


    def __ne__(self, other):
        return not (self == other)


    def __repr__(self):
        """
        """
        return "{0!s}".format(self.token.lexeme)

    __str__ = __repr__


"""
A helper classes to hold circuit statements as the same is transformed into a linked list.
This is done in order to reduce the cost of insertion of statements in a circuit.
"""
class CircuitStatement(object):
    """

    """
    stmt    : Statement     = None
    prev    : Statement     = None
    next    : Statement     = None

    def __init__(self, statement: Statement):
        self.stmt = statement
        self.prev = None
        self.next = None


class CircuitStatements(object):
    """

    """
    # I wonder if I'm not doing too much bookkeeping here
    head    : CircuitStatement      = None
    prev    : CircuitStatement      = None
    current : CircuitStatement      = None
    next    : CircuitStatement      = None
    tail    : CircuitStatement      = None
    length  : int                   = 0

    def __init__(self):
        self.head = None
        self.prev = None
        self.current = None
        self.next = None
        self.tail = None
        self.length = 0


    def append(self, statement: Statement):
        """
        """
        new = CircuitStatement(statement)

        # If this is the first element, we set it as the iterator head
        if self.head is None:
            self.head = new
            self.next = new

        # If the list is not empty, we update the tail next element
        if self.tail is not None:
            self.tail.next = new
            new.prev = self.tail
        
        self.tail = new

        # Increase the length:
        self.length = self.length + 1


    def insert(self, statements):
        """
        """
        # If the head of statements is a return statement, we don't perform any updates on the head
        if isinstance(statements.tail.stmt, ReturnStatement):
            # We double check to ensure that the current expression statement is an assignment statement
            if isinstance(self.current.stmt, (ExpressionStatement, ReturnStatement)) == False:
                raise ValueError("Expected a return statement or an expression statement as the current statement.")

            if isinstance(self.current.stmt, ExpressionStatement) and isinstance(self.current.stmt.expr, AssignmentExpression) == False:
                raise ValueError("The current expression statement to fold a return statement into must be an assignment expression statement.")

            # If we have an assignment statement
            if isinstance(self.current.stmt.expr, AssignmentExpression):
                self.current.stmt.expr.rval = statements.tail.stmt.expr

            # If we have a return statement
            if isinstance(self.current.stmt, ReturnStatement):
                self.current.stmt.expr = statements.tail.stmt.expr

            
            # # We make sure to update the pointers to the head and all that
            # if self.prev is None:
            #     self.head = statements.head
            # else:
            #     self.prev.next = statements.head
            #     statements.head.prev = self.prev

            # The list of statements contains more than one statement
            if statements.head.stmt is not statements.tail.stmt:
                statements.tail.prev.next = self.current
                self.current.prev = statements.tail.prev

        else:
            # Take care of the tail of the folded circuit
            if self.next is None:
                self.tail = statements.tail

            # We make the tail of the folded circuit point to the next statement of the current circuit
            statements.tail.next = self.next

        # Take care of the head of the folded circuit
        if self.prev is None:
            self.head = statements.head
            statements.head.prev = self.prev
        else:
            self.prev.next = statements.head

        # Update the length
        self.length = self.length + statements.length - 1


    @property
    def first(self):
        return self.head.stmt


    @property
    def last(self):
        return self.tail.stmt


    def __len__(self):
        return self.length


    def __iter__(self):
        return self


    def __next__(self):
        if self.next is None:
            self.next = self.head
            raise StopIteration

        else:
            self.prev = self.current
            self.current = self.next
            self.next = self.next.next
            return self.current.stmt
