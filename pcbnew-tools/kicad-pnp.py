#python3
import sys
from pcbnew import *

filename=sys.argv[1]
plotDir = sys.argv[2] if len(sys.argv) > 2 else "outputs/pnp/"

pcb = LoadBoard(filename)
#12: "Other", "Exclude from POS", "Exclude from BOM"
#10: "Polygon"
attributes = {1:"THT", 2:"SMD", 10:"NOC", 12:"VIR"}
side = {"True":"bot", "False":"top"}

#origin = pcb.GetAuxOrigin()
origin = [0,0]
lines = {"THT":[], "SMD":[], "VIR":[]}
lines["THT"].append(("# Ref","Val","Package","PosX","PosY","Rot","Side"))
lines["SMD"].append(("# Ref","Val","Package","PosX","PosY","Rot","Side"))
lines["VIR"].append(("# Ref","Val","Package","PosX","PosY","Rot","Side"))

for m in pcb.GetFootprints():
    coordinates = (str((m.GetCenter()[0]-origin[0])/1000.0/1000.0), str((m.GetCenter()[1]-origin[1])/1000.0/1000.0))
    #print((m.GetReference(),m.GetAttributes()))
    if not(attributes[m.GetAttributes()]=="NOC"):
        lines[attributes[m.GetAttributes()]].append((m.GetReference(), m.GetValue(), str(m.GetFPID().GetLibItemName()), coordinates[0], coordinates[1], str(int(m.GetOrientationDegrees())), side[str(m.IsFlipped())]))

for key in ["THT", "SMD", "VIR"]:
    maxlen = [0]*len(lines[key][0])
    #print(maxlen)
    for i in range(len(lines[key][0])):
        for j in range(len(lines[key])):
            maxlen[i] = max(maxlen[i], len(lines[key][j][i])+1)

    with open(plotDir+filename.rsplit('.', 1)[0]+"-"+key+".pos", 'w') as out_file:
        for line in lines[key]:
            out_line = ""
            for i in range(len(line)):
                out_line = out_line + line[i] + " "*(maxlen[i]-len(line[i]))
            out_file.write(out_line+'\n')
