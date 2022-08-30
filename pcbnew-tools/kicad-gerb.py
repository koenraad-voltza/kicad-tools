#!/usr/bin/env python2
'''
    Based on gen_gerber_and_drill_files_board.py in kicad/demos directory.
    Based on https://github.com/hzeller/ldgraphy/tree/master/pcb/kicad-scripts
    Added: gko rename, aux origin
'''

#import sys
import os
import argparse

from pcbnew import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Fabrication outputs for KiCad')
    parser.add_argument('-f', '--format', action="store", default="gerb", help='filetype: gerb/pdf (default = gerb)')
    parser.add_argument('-r', '--refdes', action="store", default="true", help='plot visible refdes (default = true)')
    parser.add_argument('input', action="store", help='input .kicad_pcb file')
    parser.add_argument('output', action="store", default="outputs/", help='input output folder (default = outputs)')
    args = parser.parse_args()

    abspathinput= os.path.abspath(args.input)
    abspathoutput= os.path.abspath(args.output)
    refdes = args.refdes.lower() in ("yes", "true", "t", "1")

    if (args.format == "pdf"):
        format = PLOT_FORMAT_PDF
    else:
        if (args.format == "dxf"):
            format = PLOT_FORMAT_DXF
        else:
            format = PLOT_FORMAT_GERBER

    #filename=sys.argv[1]
    #plotDir = sys.argv[2] if len(sys.argv) > 2 else "plot/"
    board = LoadBoard(args.input)

    nlayers = board.GetCopperLayerCount()

    pctl = PLOT_CONTROLLER(board)

    #TODO: check refill zones
    popt = pctl.GetPlotOptions()

    popt.SetOutputDirectory(args.output)

    # Set some important plot options:
    popt.SetPlotFrameRef(False)
    popt.SetLineWidth(FromMM(0.1))
    popt.SetPlotReference(refdes)		#Visible refdes are printed
    popt.SetPlotValue(True)		#Visible values are printed (eg. testpoint name)
    popt.SetPlotPadsOnSilkLayer(False)
    popt.SetAutoScale(False)
    popt.SetScale(1)
    popt.SetMirror(False)
    popt.SetExcludeEdgeLayer(False);
    popt.SetUseAuxOrigin(False)

    popt.SetUseGerberAttributes(False)
    popt.SetUseGerberProtelExtensions(False)
    popt.SetSubtractMaskFromSilk(False)

    # param 0 is the layer ID
    # param 1 is a string added to the file base name to identify the drawing
    # param 2 is a comment
    # Create filenames in a way that if they are sorted alphabetically, they
    # are shown in exactly the layering the board would look like. So
    #   gerbv *
    # just makes sense
    if (format == PLOT_FORMAT_DXF):
        plot_plan = [
            ( Edge_Cuts, "Edge_Cuts",   "Edges" ) ]
    else:
        plot_plan = [
            ( Edge_Cuts, "Edge_Cuts",   "Edges" ),

            ( F_SilkS,   "SilkTop",     "Silk top" ),
            ( F_Paste,   "PasteTop",    "Paste top" ),
            ( F_Cu,      "CuTop",       "Top layer" ),
            ( F_Mask,    "MaskTop",     "Mask top" ),

            ( B_Mask,    "MaskBottom",  "Mask bottom" ),
            ( B_Cu,      "CuBottom",    "Bottom layer" ),
            ( B_Paste,   "PasteBottom", "Paste Bottom" ),
            ( B_SilkS,   "SilkBottom",  "Silk top" ),
        ]

        if (nlayers > 2):
            plot_plan.append(( In1_Cu,    "CuIn1",       "Inner Layer1" ))
            plot_plan.append(( In2_Cu,    "CuIn2",       "Inner Layer2" ))

        if (nlayers > 4):
            plot_plan.append(( In3_Cu,    "CuIn3",       "Inner Layer3" ))
            plot_plan.append(( In4_Cu,    "CuIn4",       "Inner Layer4" ))

        if (nlayers > 6):
            plot_plan.append(( In5_Cu,    "CuIn5",       "Inner Layer5" ))
            plot_plan.append(( In6_Cu,    "CuIn6",       "Inner Layer6" ))

    for layer_info in plot_plan:
        #print("starting plot " + str(format))
        #print(layer_info)
        pctl.SetLayer(layer_info[0])
        pctl.OpenPlotfile(layer_info[1], format, layer_info[2])
        pctl.PlotLayer()

    # At the end you have to close the last plot, otherwise you don't know when
    # the object will be recycled!
    pctl.ClosePlot()
