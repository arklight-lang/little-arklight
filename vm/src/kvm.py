#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author          : Ntwali Bashige
Copyright       : Copyright 2019 - Ntwali Bashige
License         : MIT
Version         : 0.0.1
Maintainer      : Ntwali Bashige
Email           : ntwali.bashige@gmail.com
"""

"""This module runs the VM, executing the given bytecode.

This is the module that's called to start execution of the virtual machine.
It receives a file containing the bytecode as argument then calls the virtual machine execute method
to interpret the given bytecode.

Example:
    The module can be passed as argument to the Python interpreter
        $ python vm.py bytecode.kar

    Or it can be invoked directly and leave it to the terminal to invoke Python
        $ ./vm.py bytecode.kar

TODO:
    Accept the binary file containing the bytecode as argument.
"""
from common.operations import OpCode
from common.operands import OpType
from common.directives import Directives
from common.bytecode import Bytecode
from vm.vmachine import VMachine

def main():
    directives = Directives()
    directives.set_main("main")
    directives.set_regcount(1)

    bytecode = Bytecode()
    # bytecode.append(OpCode.PRINT)
    # bytecode.append(OpType.BINARY)
    # bytecode.append(10)

    vmachine = VMachine(directives, bytecode)
    vmachine.run()

if __name__ == "__main__":
    main()
