import argparse
import os
from libs.sch import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Kicad schematic variant schematic')
    parser.add_argument('input', action="store", help='Path containing input .sch file')
    parser.add_argument('variant', action="store", help='Component field name of Variant')
    args = parser.parse_args()

    ## Copy all files to variant folder
    variantpath = args.input+'/'+args.variant+'/'
    os.mkdir(variantpath)
    os.system("cp "+args.input+"/* "+variantpath)

    for file in os.listdir(variantpath):
        if file.endswith(".sch"):
            print("Processing: " + os.path.join(variantpath, file))
            sch = Schematic(variantpath+file)
            for component in sch.components:
                #print(component.fields[0]['ref'])
                #print(component.fields)
                for field in component.fields:
                    #print(field['name'].strip().lower())
                    #print(args.variant.strip().lower())
                    if args.variant.strip().lower() in field['name'].strip().lower():
                        #print(field)
                        if "no" in field['ref'].lower():
                            print("Setting component "+ component.fields[0]['ref'] + " to DNP")
                            component.fields[1]['ref']="\"DNP\""
            sch.save()
