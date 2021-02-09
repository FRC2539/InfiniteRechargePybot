from __future__ import print_function

import builtins as __builtin__

import pprint

import inspect

from commands2 import Subsystem

ALLOWPRINTS = True

printsDisabled = []

"""
This is a 'middle man' class. Subsystems should inherit from this class.
print control does indeed work, please use it. The network table crap kinda
doesn't work yet though. 

TODO: 
- Network table and subsystem integration. 
"""


def print(*args, **kwargs):
    if not inspect.stack()[1].filename in printsDisabled:
        return __builtin__.print(*args, **kwargs)


def disablePrints():
    caller = inspect.stack()[1].filename

    printsDisabled.append(str(caller))


def enablePrints():
    caller = inspect.stack()[1].filename

    try:
        printsDisabled.remove(str(caller))
    except (ValueError):
        pass


class CougarSystem(Subsystem):
    def __init__(self):
        
        super().__init__()

        self.data = {}  # Individual to each subsystem. {Name : Method}
        self.writeOnDisable = []  # [Parent, Name, Value]

        # Need to re-write the nt system.