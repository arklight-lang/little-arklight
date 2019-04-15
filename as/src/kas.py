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


"""This module runs the assembler to produce a packaged ZIP file containing the executable bytecode
and the directives file containing meta-information needed by the VM to execute the bytecode.

The assembler runs scans the given program for tokens to be passed to the parser which in turn
produces two files: bytecode and directives.json.
Then both files are packages into one ZIP file suitable for sharing and deployment.

Example:
    The assembler is called as follows
    $ kas program.alc
"""
import sys
from docopt import docopt

from asm.lexing.lexer import Lexer
from asm.parsing.parser import Parser
from asm.parsing.grammar import Grammar
from asm.checking.checker import Checker
from asm.checking.exceptions import CheckError

def main(**kwargs):
    """Get the content of the program file and begin the assembly process.

    We receive from the user a file containing the program to be assembled.
    We make sure that the file is ASCII encoded before passing it to the lexer to begin
    the assembly process.
    
    Note:
        - It would be great if in the second version we allowed interpreted assembly.
        And more important, the user should be able to see the registers change with each
        executed instruction.
    """
    program_path = kwargs.pop("program")
    directives_path = kwargs.pop("directives")
    source = ""
    directives = ""

    # Try to get the source test
    try:
        with open(program_path, 'r', encoding = "utf-8") as program_file:
            source = program_file.read()
    except OSError:
        print("The program file <" + program_path + "> could not be found. Please make sure the file exists and the user the Arklight assembler is running under has READ permissions on the file..")

    # Try to get directives data
    try:
        with open(directives_path, 'r', encoding = "utf-8") as directives_file:
            directives = directives_file.read()
    except OSError:
        print("The directives file <" + directives_path + "> could not be found. Please make sure the file exists and the user the Arklight assembler is running under has READ permissions on the file.")

    # Begin compilation
    lexer = Lexer(source)
    parser = Parser(lexer, Grammar.parselets)
    program = parser.parse()
    # print(program, end = '', flush = True)
    checker = Checker(program, directives)
    try:
        checker.check()
        print(program, end = '', flush = True)
    except CheckError as error:
        print(error)


options = """Little Arklight assembler.

Usage:
    kas.py <program> (-d <file> | --directives=<file>)
    kas.py (-h | --help)
    kas.py (-V | --version)

Options:
    -h, --help                      Show this help message.
    -V, --version                   Display the assembler version.
    -d <file>, --directives=<file>  Specify the directives file that details the VM configuration.
"""
if __name__ == "__main__":
    args = docopt(options, version = "Little Arklight assembler 0.0.1")
    main(
        program     = args["<program>"],
        directives  = args["--directives"],
    )
