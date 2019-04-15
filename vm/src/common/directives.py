# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

class Directives(object):

    """Array of bytes representing the compiled code
    
    This class holds an array that contains the bytes representing the compiled program.
    We may write this array to a file and allow any other program to read and interpret its content.

    Attributes:
        main (string): The name of the entry circuit.
        operators(array): A list of operators. Each entry is a dictionary with the operator name, size and the matrix.
        regcount(int): The number of registers to be allocated by the VM.
    """
    main = ""
    regcount = 0
    operators = []

    def set_main(self, main: str):
        """Set the name of the circuit to serve as entry point."""
        self.main = main

    def set_regcount(self, regcount: int):
        """Set the number of registers to be initialized by the VM"""
        self.regcount = regcount

    def add_operator(self, operator: dict):
        """Add an operator to the operators list"""
        self.operators.append(operator)
