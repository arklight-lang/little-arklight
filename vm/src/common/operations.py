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

class OpCode(IntEnum):
    """Enum type for supported operations codes."""
    PRINT = 0
    MOV = 1
    APPLY = 2

    def is_unary(self):
        """Returns true if the current instruction accepts a single operand

        For certain instructions, we need to be able to decide how many arguments they accept
        so we can decide how bytes to read further into the bytecode.
        """
        if self.value == 0:
            return True
        else:
            return False

    def is_binary(self):
        """Returns true if the current instruction accepts a single operand

        For certain instructions, we need to be able to decide how many arguments they accept
        so we can decide how bytes to read further into the bytecode.
        """
        if self.value  == 1:
            return True
        else:
            return False

    def is_apply(self):
        """Returns true if the current instruction is the APPLY instruction.

        For the APPLY instruction, this method is handy since the VM needs to execute generic code
        that is dependent of the matrix representation of the matrix of the operator itself.
        """
        if self.value == 2:
            return True
        else:
            return False
