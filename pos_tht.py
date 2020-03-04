#python3
import sys
from pcbnew import *

filename=sys.argv[1]

pcb = LoadBoard(filename)
attributes = {0:"THT", 1:"SMD", 2:"VIR"}
side = {True:"bot", False:"top"}

origin = pcb.GetAuxOrigin()
lines = [("# Ref","Val","Package","PosX","PosY","Rot","Side")]
for m in pcb.GetModules():
    if attributes[m.GetAttributes()]=="THT":
        #m.GetFPID().GetLibNickname()
        coordinates = (str((m.GetCenter()[0]-origin[0])/1000.0/1000.0), str((m.GetCenter()[1]-origin[1])/1000.0/1000.0))
        lines.append((m.GetReference(), m.GetValue(), str(m.GetFPID().GetLibItemName()), coordinates[0], coordinates[1], str(int(m.GetOrientationDegrees())), side[m.IsFlipped()]))
        #print(m.GetReference() + '\t' + m.GetValue() + '\t' + str(m.GetFPID().GetLibItemName()) + '\t' + coordinates + '\t' + str(int(m.GetOrientationDegrees())) + '\t' + side[m.IsFlipped()])

maxlen = [0]*len(lines[0])
#print(maxlen)
for i in range(len(lines[0])):
    for j in range(len(lines)):
        maxlen[i] = max(maxlen[i], len(lines[j][i])+1)

with open(filename.split('.')[0]+"-tht.pos", 'w') as out_file:
    for line in lines:
        out_line = ""
        for i in range(len(line)):
            out_line = out_line + line[i] + " "*(maxlen[i]-len(line[i]))
        out_file.write(out_line+'\n')
