# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from common.directives import Directives
from common.bytecode import Bytecode
from common.operations import OpCode
from common.operands import OpType
from common.exceptions import *

class VMachine(object):
    """The discrete classical virtual machine responsible for executing the bytecode.
    
    When given a bytecode, the virtual machine is reponsible for executing each instruction in it.

    Attributes:
        bytecode(Bytecode): The bytecode to execute.
        ip(int): Pointer to the instruction about to be executed.
    """
    directives = None
    bytecode = None
    ip = 0

    # Private data that should never accessible outside of the VM
    # A dictionary that maps register names to their values
    _registers = {}
    # A dictionary that maps operator indices to their input size and matrices
    _operators = {}

    def __init__(self, directives: Directives,  bytecode: Bytecode):
        self.directives = directives
        self.bytecode = bytecode

        # We initialize the VM by allocating registers
        self.init()

    def init(self):
        """Create an array of registers to be used by the VM and name them."""
        # Make sure we have at least one register to work with
        if self.directives.regcount == 0:
            raise ValueError("The number of registers to initialize the VM with cannot be zero.")

        # Initialize as many registers as there are regcount(s)
        regindex = 1
        while regindex <= self.directives.regcount:
            self._registers["r" + str(regindex)] = None # None to be replaced with numpy vector
            regindex = regindex + 1

        # Set operators by mapping their names to their input size and matrix
        opindex = 0
        for opindex, opvalue in enumerate(self.directives.operators):
            self._operators[opvalue.id] = (opvalue.size, opvalue.matrix)

    def run(self):
        """A big if...elif...else that fetches each instruction and performs the required side effect.

        Note:
            - In the future, explore the possibility of using a jump table or other ways to speed up execution.
        """
        while True:
            instruction = self.bytecode.code[self.ip]

            if instruction == OpCode.PRINT:
                self._run_print()

            elif instruction == OpCode.APPLY:
                self._run_apply()

            else:
                raise RuntimeError("Unknown instruction found at offset <" + str(self.ip) + "> on line <" + str(self.bytecode.lines[self.ip]) + ">.")

            # If the instruction pointer points beyond the bytecode boundaries, we terminate execution
            if self.ip == self.bytecode.length():
                break

    def _run_print(self):
        """Execute the print instruction to output the given value to standard output.

        The print instruction expects the type of input as first byte after the instruction byte
        and the input value byte after the input type byte.

        Format:
            instruction_byte[ip + 0] input_type[ip + 1] input_value[ip + 2]
        """
        instruction = self.bytecode.code[self.ip]
        input_type = self.bytecode.code[self.ip + 1]
        input_value = self.bytecode.code[self.ip + 2]

        # If the value to print is inside a register, we fetch the value at the given register index
        if input_type == OpType.REGISTER:
            print("Printing value from register.")

        # If the value to print is binary literal, we print it directly
        elif input_type == OpType.BINARY:
            print("Printing binary literal.")

        # Anything else is an error
        else:
            raise ValueError("Unexpected input type to be printed at offset <" + str(self.ip + 1) + ">.")

        # Update the instruction pointer to the next instruction
        self.ip = self.ip + 3

    def _run_apply(self):
        """Execute the apply instruction which role is to perform a matrix multiplication (representing the operator) with the input.

        The apply instruction needs to be aware of the input size and it fetches the same from the operator.
        The complete format is found below with a simplified format of: instruction_byte > operator_byte > input_bytes > output_bytes.
        The operator_byte holds the operator ID that is used to fetch the operator to execute from the self._operators dictionary.

        Format:
            instruction_byte[ip + 0] operator_byte[ip + 1] input_bytes[2..n] output_bytes[n+1..n+2]
            input_bytes = input_type input_value
        """
        self.ip = self.ip + 1
        operator_id = self.bytecode.code[self.ip]

        # Fetch the operator details so we know two things: which operator to execute and how many bytes to read for the input
        input_size, operator = self._operators[operator_id]
        
        # Read the input
        inputs = []
        input_index = 0
        input_data = None
        self.ip = self.ip + 2
        while input_index < input_size:
            input_data = (self.bytecode.code[self.ip + input_index], self.bytecode.code[self.ip + input_index + 1])

        # Read the output
        self.ip = self.ip + input_index + 1
        output_data = (self.bytecode.code[self.ip], self.bytecode.code[self.ip + 1])

        # Validate the output
        # The output type must always be a register
        if output_data[0] != OpType.REGISTER:
            raise ValueError("Unexpected output operand at offset <" + str(self.bytecode.code[self.ip]) + ">. Expected a register.")
        # The output register must be within the VM register count
        if output_data[1] >= len(self._registers):
            raise ValueError("Output register outside of VM register count. Byte at offset <" + str(self.bytecode.code[self.ip + 1]) + ">.")

        # Execute the instruction
        print("Executing the APPLY instruction.")

        # Update the instruction pointer to the next instruction
        self.ip = self.ip + 2
