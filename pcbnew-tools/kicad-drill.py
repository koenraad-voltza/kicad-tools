#!/usr/bin/env python2
'''
    Based on gen_gerber_and_drill_files_board.py in kicad/demos directory.
    Based on https://github.com/hzeller/ldgraphy/tree/master/pcb/kicad-scripts
    Added: gko rename, aux origin
'''

import sys
import os

from pcbnew import *
filename=sys.argv[1]
plotDir = sys.argv[2] if len(sys.argv) > 2 else "outputs/drill/"

board = LoadBoard(filename)

# Fabricators need drill files.
# sometimes a drill map file is asked (for verification purpose)
drlwriter = EXCELLON_WRITER( board )
drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )

mirror = False
minimalHeader = False
offset = board.GetAuxOrigin()
mergeNPTH = False   # non-plated through-hole
drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

metricFmt = True
drlwriter.SetFormat( metricFmt )

genDrl = True
genMap = True
drlwriter.CreateDrillandMapFilesSet( plotDir, genDrl, genMap );
