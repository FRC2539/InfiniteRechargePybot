from commands2 import SequentialCommandGroup

from commands.autonomouscommandgroup import AutonomousCommandGroup

from custom import driverhud

from networktables import NetworkTables

excludedMethods = [
    "interrupted"
]  # Methods that aren't from the parents but aren't autos.

table = NetworkTables.getTable("Autonomous")
autoVars = [var.lower() for var in dir(AutonomousCommandGroup)]

definedAutos = []
for auto in autoVars:
    if (
        auto[0] != "_"
        and auto not in [var.lower() for var in dir(SequentialCommandGroup)]
        and auto not in excludedMethods
    ):
        definedAutos.append(auto)


def init():
    table.putStringArray("autos", [a.lower() for a in definedAutos])


def getAutoProgram():
    try:
        return table.getString("selectedAuto", (definedAutos[0]).lower())
    except (IndexError):
        return table.getString("selectedAuto")
