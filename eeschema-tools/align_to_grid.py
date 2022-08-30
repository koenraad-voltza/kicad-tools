#must be run with python3
import argparse
from libs.sch import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align components in Kicad schematic sheet to grid')
    parser.add_argument('file', action="store", help='EESchema file (.sch)')
    parser.add_argument('--grid', '-g', action="store", default="100", help='grid size (mil)')
    args = parser.parse_args()

    sch = Schematic(args.file)
    for component in sch.components:
        changed = False
        oldcoordinates = (component.fields[0]['posx'], component.fields[0]['posy'])
        if not((int(component.fields[0]['posx']) % int(args.grid))==0):
            changed = True
            component.fields[0]['posx'] = str(int((round(int(component.fields[0]['posx']) / float(args.grid))*int(args.grid))))
            #print(int(component.fields[0]['posx']))
        if not((int(component.fields[0]['posy']) % int(args.grid))==0):
            changed = True
            component.fields[0]['posy'] = str(int((round(int(component.fields[0]['posy']) / float(args.grid))*int(args.grid))))
        if changed == True:
            newcoordinates = (component.fields[0]['posx'], component.fields[0]['posy'])
            print("Changed component " + component.fields[0]["ref"] + "from " + str(oldcoordinates) + " to " + str(newcoordinates))
    sch.save()
