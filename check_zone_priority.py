#python3
import sys
from pcbnew import *

filename=sys.argv[1]

pcb = LoadBoard(filename)
zones={}
layers={0:"TOP", 31:"BOT"}
for zone in pcb.Zones():
    zonesummary = (zone.GetPriority(), zone.GetNetname())
    if (zone.GetLayer() in zones.keys()):
        zones[zone.GetLayer()].append(zonesummary)
    else:
        zones[zone.GetLayer()] = [zonesummary]

for layer in zones.keys():
    if layer in layers.keys():
        print("Layer: " + layers[layer])
    else:
        print("Unknown Layer: " + str(layer))
    zones[layer].sort(key=lambda tup: tup[0])
    for zone in zones[layer]:
        print("* Zone: " + str(zone[0]) +":" + zone[1])
    print("")

#TODO: fix zones
#pcb.Save("mod_"+filename)
