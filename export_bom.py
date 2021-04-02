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
    args = parser.parse_args()
    abspathinput= os.path.abspath(args.input)
    abspathoutput= os.path.abspath(args.output)
    projectname = abspathinput.split('/')[-1].split('.')[0]
    export_bom(abspathinput, abspathoutput)
    os.system("rm " + abspathoutput +"/export_bom_screencast.ogv")
    os.system("mv "+ abspathinput.split('.')[0] + ".csv "+ abspathoutput +'/'+projectname+".pdf")
