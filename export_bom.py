#!/usr/bin/env python

#   Copyright 2015-2016 Scott Bezek and the splitflap contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
import os
import subprocess
import sys
import time
import argparse
import re
from libs.sch import *

from contextlib import contextmanager

electronics_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repo_root = os.path.dirname(electronics_root)
sys.path.append(repo_root)

from export_util import (
    PopenContext,
    xdotool,
    wait_for_window,
    recorded_xvfb,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def eeschema_export_bom(output_directory):
    wait_for_window('eeschema', '\[')

    logger.info('Focus main eeschema window')
    xdotool(['search', '--name', '\[', 'windowfocus'])

    logger.info('Open Tools->Generate Bill Of Materials')
    xdotool(['key', 'alt+t'])
    xdotool(['key', 'm'])

    logger.info('Run generate')
    wait_for_window('plot', 'Bill of Material')
    xdotool(['search', '--name', 'Bill of Material', 'windowfocus'])
    xdotool(['key', 'Return'])

    logger.info('Wait before shutdown')
    time.sleep(2)

def export_bom(schematic_file, output_dir):
    screencast_output_file = os.path.join(output_dir, 'export_bom_screencast.ogv')

    with recorded_xvfb(screencast_output_file, width=800, height=600, colordepth=24):
        with PopenContext(['eeschema', schematic_file], close_fds=True) as eeschema_proc:
            eeschema_export_bom(output_dir)
            eeschema_proc.terminate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Kicad BOM')
    parser.add_argument('input', action="store", help='input .sch file')
    parser.add_argument('output', action="store", help='output folder')
    parser.add_argument('-v', '--variant', action="store", default='None', help='Component field name of Variant')
    args = parser.parse_args()

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

    # TODO check if kicad is still running (script may fail)
    export_bom(variantpath + projectname+".sch", abspathoutput)
    os.system("rm " + abspathoutput +"/export_bom_screencast.ogv")
    os.system("mv "+ variantpath + projectname+".csv "+ abspathoutput +'/'+projectname+"_"+args.variant+".csv")
