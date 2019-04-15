# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

import json

from common.ast import *
from asm.checking.exceptions import CheckError

class Checker(object):
    """
    """
    program         : Program       = None
    _special_gates  : list          = []
    _circuits       : set           = set([])
    _circuit        : list          = []

    directives      : dict          = {}
    _reg_count      : dict          = {}
    _reg_prefix     : dict          = {}
    _gates          : dict          = {}
    _all_prefix     : set           = set([])


    def __init__(self, program: Program, directives: str):
        self.program = program
        self._special_gates = ['print']
        self._circuits = set([])
        self._circuit = []

        self.directives = json.loads(directives)
        self._reg_count = {}
        self._reg_prefix = {}
        self._gates = {}
        self._all_prefix = set([])


    def check(self):
        """
        """
        # Check directives
        self._checkDirectives()

        # Check the program
        self._checkProgram()


    def _checkDirectives(self):
        """
        """
        keys = self.directives.keys()

        # if isinstance(keys, str) == False:
        #     raise CheckError("[Checking Error] Expected the key indicating directives for the virtual machine to be a string.")

        if "cvm/deterministic" in keys:
            self._checkDeterministic()

        elif "cvm/stochastic" in keys:
            raise CheckError("[Checking Error] No stochastic virtual machine is not supported at the moment.")

        elif "qvm/discrete" in keys:
            raise CheckError("[Checking Error] No discrete variables quantum virtual machine is not supported at the moment.")

        elif "qvm/continuous" in keys:
            raise CheckError("[Checking Error] No continuous variables quantum virtual machine is not supported at the moment.")

        elif "qvm/adiabatic" in keys:
            raise CheckError("[Checking Error] No adiabatic quantum virtual machine is not supported at the moment.")

        else:
            raise CheckError("[Checking Error] Please provide a valid virtual machine identifier.")


    def _checkDeterministic(self):
        """
        """
        vm_id = "cvm/deterministic"

        # We narrow directives to that of a classical deterministic virtual machine
        directives = self.directives[vm_id]

        # We check the count of registers making sure that is not zero
        if "reg-count" not in directives.keys():
            raise CheckError("[Checking Error] The register count for <" + vm_id + "> is missing, please provide one.")

        reg_count = directives["reg-count"]
        if isinstance(reg_count, int) == False:
            raise CheckError("[Checking Error] The register count for <" + vm_id + "> must be an integer.")

        if reg_count <= 0:
            raise CheckError("[Checking Error] The register count for <" + vm_id + "> must be greater than zero.")

        self._reg_count[vm_id] = reg_count

        # If the register width was provided, we raise an error since right now we only support register with width of 1
        if "reg-width" in directives.keys():
            raise CheckError("[Checking Error] Only registers of width 1 are supported at the moment.")

        # We ensure that the register prefix is not used for any other virtual machine
        if "reg-prefix" not in directives.keys():
            raise CheckError("[Checking Error] The register prefix for <" + vm_id + "> is missing, please provide one.")

        reg_prefix = directives["reg-prefix"]
        if isinstance(reg_prefix, str) == False:
            raise CheckError("[Checking Error] The register prefix for <" + vm_id + "> must be a string.")

        if reg_prefix in self._all_prefix:
            raise CheckError("[Checking Error] The register prefix for <" + vm_id + "> is already used by another virtual machine.")

        self._all_prefix.add(reg_prefix)
        self._reg_prefix[vm_id] = reg_prefix


        # Checking gates:
        #   We make sure that they all 




    def _checkProgram(self):
        """
        """
        main = self.program.get_main()
        
        # Validate the main circuit and in the process all the circuits that it depends on, directly or indirectly
        self._checkMain(main)

        # We delete all other circuits other than main since they will have been absorbed into main
        self.program.clean()


    def _checkMain(self, main: CircuitDeclaration):
        """
        """
        # The main circuit should not accept any arguments
        params = main.params
        if len(params) > 0:
            raise CheckError("[Checking Error] The main circuit cannot accept any arguments.")

        # We check main circuit
        self._checkCircuitDeclaration(main)


    def _checkCircuitDeclaration(self, circuit: CircuitDeclaration):
        """
        """
        # If it was not being folded yet, it is being folded now so we add it
        self._circuits.add(circuit.token.lexeme)

        # Push the current circuit to the circuit stack
        self._circuit.append(circuit)

        # Check one statement. For now, only expressions statements are available
        stmts = circuit.stmts
        if len(stmts) == 0:
            raise CheckError("[Checking Error] A circuit declaration cannot be empty. Circuit declared on line <" + str(circuit.token.line) + "> is empty.")

        for stmt in stmts:
            new_circuit = self._checkStatement(stmt)
            if new_circuit is not None:
                # We begin by checking if the current statement is an assignment expression statement
                #   If that is the case, we make sure that the new circuit ends with a return statement
                if (isinstance(stmt, ExpressionStatement) and isinstance(stmt.expr, AssignmentExpression)) or isinstance(stmt, ReturnStatement):
                    if isinstance(new_circuit.stmts.last, ReturnStatement) == False:
                        if isinstance(stmt, ExpressionStatement):
                            raise CheckError("[Checking Error] The circuit that appears as rval to the assignment expression must return an expression. Line <" + str(stmt.expr.token.line) + ">.")
                        elif isinstance(stmt, ReturnStatement):
                            raise CheckError("[Checking Error] The circuit that is to be returned from the current return statement must return an expression. Line <" + str(stmt.expr.token.line) + ">.")
                
                # We proceed to insert the folded circuit into the current circuit
                self._checkCircuitDeclaration(new_circuit)
                circuit.stmts.insert(new_circuit.stmts)

        # Pop the circuit from the circuit stack as we are done here
        self._circuit.pop()

        # We are done folding the circuit, we remove it from the list of circuits being folded
        self._circuits.remove(circuit.token.lexeme)


    def _checkStatement(self, statement: Statement):
        """
        """
        if isinstance(statement, ReturnStatement):
            return self._checkReturnStatement(statement)

        elif isinstance(statement, ExpressionStatement):
            expr = statement.expr
            return self._checkExpression(expr)

        else:
            raise CheckError("[Checking Error] Only expression statements are supported at the moment but a different statement was found on line <" + str(statement.token.line) + ">.")


    def _checkReturnStatement(self, statement: ReturnStatement):
        """
        """
        expr = statement.expr

        # We can't return from main
        if self._circuit[-1].token.lexeme == "main":
            raise CheckError("[Checking Error] A return statement is not allowed inside the main circuit. Line <" +  + str(statement.token.line) + ">.")

        # Only register, gate and circuit expressions can be return
        if isinstance(expr, (RegisterExpression, GateExpression, CircuitExpression)) == False:
            raise CheckError("[Checking Error] Only register (parameters) and gate (circuits) expressions can be returned from a circuit. Line <" + str(statement.token.line) + ">.")

        # If the returned expression is a circuit expression, we fold it
        if isinstance(expr, CircuitExpression):
            return self._checkCircuitExpression(expr)

        else:
            return None

        # Only deterministic registers and gate values can be returned from
        # ...


    def _checkExpression(self, expression: Expression):
        """
        """
        if isinstance(expression, AssignmentExpression):
            return self._checkAssignmentExpression(expression)

        elif isinstance(expression, CircuitExpression):
            return self._checkCircuitExpression(expression)

        elif isinstance(expression, GateExpression):
            return self._checkGateExpression(expression)

        elif isinstance(expression, ParameterExpression):
            return self._checkParameterExpression(expression)

        elif isinstance(expression, RegisterExpression):
            return self._checkRegisterExpression(expression)

        elif isinstance(expression, LiteralExpression):
            return self._checkLiteralExpression(expression)

        else:
            raise CheckError("[Checking Error] Unexpected expression found on line <" + expression.token.line + ">.")


    def _checkAssignmentExpression(self, expression: AssignmentExpression):
        """
        """
        lval = expression.lval
        rval = expression.rval

        # We require that the lval always be a register expression
        if isinstance(lval, RegisterExpression) == False:
            raise CheckError("[Checking Error] The lval of an assignment expression must always be a register expression.")

        # We require that rval be one of:
        #   - circuit expression
        #   - gate expression
        #   - register expression
        #   - literal expression
        if isinstance(rval, (CircuitExpression, GateExpression, RegisterExpression, LiteralExpression)) == False:
            raise CheckError("[Checking Error] The rval of an assignment expression must be either a gate expression, a register expression or a literal expression. The offending expression is on line <" + str(rval.token.line) + ">.")

        # If the rval is a gate expression, we make sure it is not one of from a select set of built in instructions whose results are not movable (they don't return values)
        #   The instruction PRINT and all other JUMP instructions will not result in a general purpose register being modified so we prevent them from being rvals
        if isinstance(rval, GateExpression) and rval.token.lexeme.lower() in self._special_gates:
            raise CheckError("[Checking Error] The <" + rval.token.lexeme.lower() + "> instruction cannot be an rval of assignment expression on line <" + str(rval.token.line) + ">.")

        # If the rval is a circuit expression, we make sure to fold it and return the folded circuit
        if isinstance(rval, CircuitExpression):
            return self._checkCircuitExpression(rval)

        else:
            return None

        # We make sure that the lval and rval are of the same kind as in classical-classical
        #   ... Since we are not given the directive data yet, we eschew this step for the moment


    def _checkCircuitExpression(self, expression: CircuitExpression):
        """
        """
        # We make sure that each argument passed to the circuit is a register expression
        args = expression.args
        for arg in args:
            if isinstance(arg, RegisterExpression) == False:
                raise CheckError("[Checking Error] Expected a register as argument to a circuit on line <" + str(arg.token.line) + ">.")

        # We validate the declaration
        #   We make sure that there exist a circuit by the given name and arity
        #   We make the appropriate replacements of paramaters by the given arguments
        #   Then we call the circuit declaration validator to validate the correctly formed circuit declaration
        try:
            circuit = self.program.get_declaration(expression.token.lexeme, len(args))

            # Start the folding process
            new_circuit = self._foldCircuit(expression, circuit)

            # We return the new circuit so its statements may be integrated into the parent circuit
            return new_circuit
        except KeyError:
            raise CheckError("[Checking Error] Failed to find a circuit by the name <" + expression.token.lexeme + "> that accepts <" + str(len(args)) + "> arguments. Circuit invoked on line <" + str(expression.token.line) + ">.")


    def _checkGateExpression(self, expression: GateExpression):
        """
        """
        # We make sure that each argument passed to the gate is a register expression
        args = expression.args
        for arg in args:
            if isinstance(arg, RegisterExpression) == False:
                raise CheckError("[Checking Error] Expected a register as argument to a gate on line <" + arg.token.line + ">.")

        # Make sure that there exists a gate by the given name and arity

        # We return None as checking gate expressions doesn't result in a new circuit
        return None


    def _checkParameterExpression(self, expression: ParameterExpression):
        """
        """
        # Parameter expression cannot occur inside the main circuit

        # We return None as checking parameter expressions doesn't result in a new circuit
        return None


    def _checkRegisterExpression(self, expression: RegisterExpression):
        """
        """
        # Make sure the register used is within the register count that will be allocated by the VM.

        # We return None as checking register expressions doesn't result in a new circuit
        return None


    def _checkLiteralExpression(self, expression: LiteralExpression):
        """
        """
        # If the top circuit is not main, it cannot use literals in to initialize registers
        if self._circuit[-1].token.lexeme != "main":
            raise CheckError("[Checking Error] Literals cannot be used to initialize registers outside of the main circuit. This occured in circuit <" + self._circuit[-1].token.lexeme + "> on line <" + str(expression.token.line) + ">.")

        # We return None as checking register expressions doesn't result in a new circuit
        return None


    def _foldCircuit(self, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """Find all paramaters in the given circuit and replace them with the given arguments.
        Return a new circuit that doesn't have any parameters but only valid statements.
        """
        # We begin by making sure that the given circuit is not already being folded to avoid recursive calls which is not allowed for circuits
        if circuit.token.lexeme in self._circuits:
            raise CheckError("[Checking Error] Circuit <" + circuit.token.lexeme + "> declared on line <" + str(circuit.token.line) + "> cannot be called within <" + self._circuit[-1].token.lexeme + "> on line <" + str(circuit_expression.token.line) + "> because it will lead to recursive circuits which is not allowed.")

        # We create a new circuit declaration with all parameters replaced by arguments
        new_circuit = CircuitDeclaration(circuit.token)
        stmts = circuit.stmts
        for stmt in stmts:
            new_circuit.add_statement(self._foldStatement(stmt, circuit_expression, circuit))

        # We have the new circuit, we return it
        return new_circuit


    def _foldStatement(self, statement: Statement, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        if isinstance(statement, ReturnStatement):
            return ReturnStatement(statement.token, self._foldExpression(statement.expr, circuit_expression, circuit))

        elif isinstance(statement, ExpressionStatement):
            return ExpressionStatement(self._foldExpression(statement.expr, circuit_expression, circuit))

        else:
            raise CheckError("[Checking Error] Only expression statements are supported at the moment but a different statement was found on line <" + str(statement.token.line) + ">.")


    def _foldExpression(self, expression: Expression, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        if isinstance(expression, AssignmentExpression):
            return self._foldAssignmentExpression(expression, circuit_expression, circuit)

        elif isinstance(expression, CircuitExpression):
            return self._foldCircuitExpression(expression, circuit_expression, circuit)

        elif isinstance(expression, GateExpression):
            return self._foldGateExpression(expression, circuit_expression, circuit)

        elif isinstance(expression, ParameterExpression):
            return self._foldParameterExpression(expression, circuit_expression, circuit)

        elif isinstance(expression, RegisterExpression):
            # Should we disallow the use of the register expressions inside the a subcircuit?
            #   This would eliminate errors where a register is used inadvently but also prevent concise code.
            #   I think it might be best to just allow it and let users write better code themselves.
            return self._foldRegisterExpression(expression, circuit_expression)

        elif isinstance(expression, LiteralExpression):
            return self._foldLiteralExpression(expression, circuit_expression)

        else:
            raise CheckError("[Checking Error] Unexpected expression found on line <" + expression.token.line + ">.")


    def _foldAssignmentExpression(self, expression: AssignmentExpression, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        # Build a new assignment expression
        new_lval = self._foldExpression(expression.lval, circuit_expression, circuit)
        new_rval = self._foldExpression(expression.rval, circuit_expression, circuit)
        new_expression = AssignmentExpression(expression.token, new_lval, new_rval)

        # Assuming all went well, we return the new assignment
        return new_expression


    def _foldCircuitExpression(self, expression: CircuitExpression, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        # Build the new circuit expression
        new_expression = CircuitExpression(expression.token)
        args = expression.args
        for arg in args:
            new_expression.add_argument(self._foldExpression(arg, circuit_expression, circuit))

        # All went well, we return
        return new_expression


    def _foldGateExpression(self, expression: GateExpression, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        # Build the new gate expression
        new_expression = GateExpression(expression.token)
        args = expression.args
        for arg in args:
            new_expression.add_argument(self._foldExpression(arg, circuit_expression, circuit))

        # All went well, we return
        return new_expression


    def _foldParameterExpression(self, expression: ParameterExpression, circuit_expression: CircuitExpression, circuit: CircuitDeclaration):
        """
        """
        # We have a parameter expression, we find its index in the circuit currently being checked
        param_index = 0
        try:
            param_index = circuit.params.index(expression)
        except ValueError:
            raise CheckError("[Checking Error] Parameter <" + expression.token.lexeme + "> on line <" + str(expression.token.line) + "> could not be transformed into a register since it is not a valid parameter of the current circuit <" + circuit.token.lexeme + ">.")

        # We use the index on the arguments given to the circuit expression to find the register to use
        reg = circuit_expression.args[param_index]

        # We create a new register expression out of the parameter expression
        new_expression = RegisterExpression(reg.token)

        # All went well, we bail out
        return new_expression


    def _foldRegisterExpression(self, expression: RegisterExpression, circuit_expression: CircuitExpression):
        """
        """
        return expression


    def _foldLiteralExpression(self, expression: LiteralExpression, circuit_expression: CircuitExpression):
        """
        """
        return expression
