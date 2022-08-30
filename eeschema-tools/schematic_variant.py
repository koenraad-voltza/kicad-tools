import argparse
import os
from libs.sch import *
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Kicad schematic variant schematic')
    parser.add_argument('-i', '--input', action="store",  default=os.getcwd(), help='input .sch file')
    parser.add_argument('output', action="store", help='output folder')
    parser.add_argument('-v', '--variant', action="store", default='None', help='Component field name of Variant')
    args = parser.parse_args()
    ## TODO option to have blank variant

    ## TODO check if variant exists

    # Get the path
    abspathinput= os.path.abspath(args.input)
    abspathoutput= os.path.abspath(args.output)
    path = '/'.join(abspathinput.split('/')[:-1])
    if abspathinput.split('.')[-1] in ['sch', 'pro']:
        projectname = '.'.join(abspathinput.split('/')[-1].split('.')[:-1])
    else:
        projectname = abspathinput.split('/')[-1]

    ## Copy all files to variant folder
    if args.variant!='None':
        variantpath = path+'/'+args.variant+'/'
        os.mkdir(variantpath)
        print("cp "+re.escape(path+"/*")+" "+re.escape(variantpath))
        os.system("cp "+re.escape(path)+"/* "+re.escape(variantpath))

        for file in os.listdir(variantpath):
            if file.endswith(".pro"):
                os.system("mv \""+variantpath+file + "\" \""+variantpath+file[:-4]+"_"+args.variant+".pro\"")
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
                            ##For population options
                            #if "no" in field['ref'].lower():
                            #    print("Setting component "+ component.fields[0]['ref'] + " to DNP")
                            #    component.fields[1]['ref']="\"DNP\""
                            ##For value changes
                            if not component.fields[1]['ref']==field['ref']:
                                if not ("yes" in field['ref'].lower()):
                                    #print(field['ref'].strip().lower())
                                    if ("no" in field['ref'].lower()) or ("dnp" in field['ref'].lower()):
                                        print("Setting component "+ component.fields[0]['ref'] + " to DNP")
                                        component.fields[1]['ref']="\"DNP\""
                                    else:
                                        print("Setting component "+ component.fields[0]['ref'] + " to "+field['ref'])
                                        component.fields[1]['ref']=field['ref']
                sch.save()
    else:
        variantpath = path+'/'
    ## Generate schematic

    # TODO check if kicad is still running (script may fail)
    os.chdir("/home/voltza/repositories/voltza-github/tools/kicad-tools/") #TODO fixme
    print("python -m eeschema.schematic export -f pdf -a \"" + variantpath + projectname+".sch\" \"" + abspathoutput+ "\"")
    os.system("python -m eeschema.schematic export -f pdf -a \"" + variantpath + projectname+".sch\" \"" + abspathoutput+"\"")
    os.system("rm \"" + abspathoutput +"/export_schematic_screencast.ogv\"")
    if args.variant!='None':
        os.system("mv \""+ abspathoutput +"/"+projectname + ".pdf\" \""+ abspathoutput +'/'+projectname+"_"+args.variant+".pdf\"")
    #TODO check if pdf was created

    ##TODO BOM?
    #python "/usr/share/kicad/plugins/bom_csv_voltza.py" pihat-power.xml pihat-power-varpi3.csv

    #os.system("rm -r " + variantpath)
