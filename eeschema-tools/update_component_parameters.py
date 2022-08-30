import argparse
import os
from libs.sch import *

def update_components(schematicfile, pn_field_name):
    #TODO Open library_file

    sch = Schematic(schematicfile)

    for component in sch.components:
        # check if is power related component
        if '#PWR' in component.fields[0]['ref'] or\
           'PWR_FLAG' in component.fields[1]['ref']:
            continue

        # reference_field = 0, value_field = 1, footprint_field = 2, datasheet_field = 3, user_defined_fields = 4..
        # get or create the PN field
        for field in component.fields:
            if field['name'].replace('"', '') == pn_field_name:
                mpn = field['ref']
                break
        else:
            print "Component " + component.fields[0]['ref'] + " does not have a MPN defined"
            mpn = raw_input("Enter MPN or press [Enter] to skip: ")
            if mpn.strip() == '':
                continue
            field = component.addField({'name': '"%s"' % pn_field_name, 'ref': mpn.strip()})

        print "Component " + component.fields[0]['ref'] + " " + mpn

        if mpn in library:
            #Check and add (or replace) additional field values
            for key in library[mpn]:
                if key == 'footprint':
                    if component.fields[2]['ref'] != library[mpn][key]:
                        print "\t Replacing " + key + ":" + field['ref']
                        print "\t With " + key + ":" + library[mpn][key]
                        if (raw_input("Replace? (Y/n)").strip().lower()[0] != 'n'):
                            component.fields[2]['ref'] = library[mpn][key]
                elif key == 'datasheet':
                    if component.fields[3]['ref'] != library[mpn][key]:
                        print "\t Replacing " + key + ":" + field['ref']
                        print "\t With " + key + ":" + library[mpn][key]
                        if (raw_input("Replace? (Y/n)").strip().lower()[0] != 'n'):
                            component.fields[3]['ref'] = library[mpn][key]
                else:
                    for field in component.fields:
                        if field['name'].replace('"', '') == key:
                            if field['ref'] != library[mpn][key]:
                                print "\t Replacing " + key + ":" + field['ref']
                                print "\t With " + key + ":" + library[mpn][key]
                                if (raw_input("Replace? (Y/n)").strip().lower()[0] != 'n'):
                                    field['ref'] = library[mpn][key]
                                break
                    else:
                        print "\t Adding " + key + ":" + library[mpn][key]
                        if (raw_input("Add? (Y/n)").strip().lower()[0] != 'n'):
                            field = component.addField({'name': key , 'ref': library[mpn][key]})
        else:
            print "MPN: " + mpn + "not found in library"
            #TODO add component
    sch.save()

# def create_component(component):
#   TODO create json file per component based on parameters, farnell json, user input

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Kicad schematic component parameters')
    parser.add_argument('input', action="store", help='Path containing input .sch files')
    parser.add_argument('--output', '-o', action="store", help='Path containing output .sch files')
    parser.add_argument('--library', '-l', action="store", default="library.json",
                       help='location of the library json file')
    parser.add_argument('--pn-field-name', help='defines the part number field name that will be used in the sch files', action='store', default='MPN')
    args = parser.parse_args()

    output_folder = args.output     #TODO: not used
    library_file = args.library

    for file in os.listdir(args.input):
        if file.endswith(".sch"):
            print "Processing: " + os.path.join(args.input, file)
            update_components(os.path.join(args.input, file), library_file)
