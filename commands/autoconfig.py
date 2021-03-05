from networktables import NetworkTables

autos = ['Example']

global table 

table = NetworkTables.getTable("Autonomous")

def compileAutos():
    for auto in autos:
        if type(auto) != str:
            raise Exception('One of the autos is NOT A string! It looks like this one: ' + str(auto))
        
