from __future__ import print_function

import builtins as __builtin__

import pprint

import inspect

from commands2 import SubsystemBase

from networktables import NetworkTables

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
    

class CougarSystem(SubsystemBase):

    intialized = False
    
    def __init__(self, subsystemName="Unknown Subsystem"):
        
        super().__init__()

        self.tableName = subsystemName
        self.table = NetworkTables.getTable(self.tableName)

        # Need to re-write the nt system.
                        
        if not CougarSystem.intialized:
            self.intializeNTServer()
            CougarSystem.intialized = True 
            
    def intializeNTServer(self):
        NetworkTables.initialize(server="roborio-2539-frc.local")
        
    def put(self, valueName, value):
        try:
            self.table.putValue(valueName, value)
            
        except: # Must be a list or tuple.
            
            try:
                if type(value[0]) is bool:
                    self.table.putBooleanArray(valueName, value)
                    
                if type(value[0]) is str:
                    self.table.putStringArray(valueName, value)
                    
                else:
                    self.table.putNumberArray(valueName, value)
                    
            except(TypeError):
                raise Exception("Unrecognizable Data Type . . . \nShould be a: boolean, int, float, string, list of bools, \nlist of strings, list of numbers.")
            
    def get(self, valueName):
        return self.table.getValue(valueName, None) # Returns None if it doesn't exist.

    def hasChanged(self, valueName, compareTo):
        if compareTo is None:
            return True
        return not self.table.getValue(valueName, None) == compareTo
    
    def delete(self, valueName):
        self.table.delete(valueName)
