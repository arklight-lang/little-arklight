# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

from common.operations import OpCode

class Bytecode(object):
    """Array of bytes representing the compiled code
    
    This class holds an array that contains the bytes representing the compiled program.
    We may write this array to a file and allow any other program to read and interpret its content.

    Attributes:
        code (bytearray): An array holding integers of bounded between 0 and 255.

    Note:
        - Think about implementing a buffered append so that we do not need to append a single byte at a time.
        - Add method to load bytecode from a file.
    """
    code = bytearray()

    def length(self):
        """Retuns the number of bytes held in the bytecode"""
        return len(self.code)

    def append(self, byte):
        """This method appends a new byte to the bytecode.

        As we receive new bytes, this method validates the new byte and append it to the bytecode.

        Args:
            byte(OpCode|int): The byte to append to the bytecode

        Raises:
            ValueError: If byte is not an integer between 0 and 255
        """
        # If we are given an opcode directly but not as an integer, we convert it to an integer
        if isinstance(byte, OpCode) == True:
            byte = int(byte)

        # Make sure the byte is an integer
        if isinstance(byte, int) == False:
            raise ValueError("Invalid byte to write to bytecode: <" + str(byte) + ">. Expected an integer.")
        
        # Make sure the byte is within a bytearray limits
        if byte < 0 or byte > 255:
                raise ValueError("Invalid byte to write to bytecode: <" + str(byte) + ">. Byte not within bounds.")

        # Write the byte into the bytearray
        self.code.append(byte)
