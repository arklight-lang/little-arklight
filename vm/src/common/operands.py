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

class OpType(IntEnum):
    """Enum type for supported operands."""
    REGISTER = 0
    BINARY = 1
