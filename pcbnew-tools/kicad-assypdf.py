#!/usr/bin/env python2

import sys
import os

from pcbnew import *

filename=sys.argv[1]
plotDir = sys.argv[2] if len(sys.argv) > 2 else "plot/"

board = LoadBoard(filename)

for module in board.GetModules():
    gfx = module.GraphicalItems()

    fabrefdes=False

    for g in gfx:
        if isinstance (g, TEXTE_MODULE):
            layer = g.GetLayer()
            if (layer == B_Fab) or (layer == F_Fab):
                if not (g.GetText()=="%R"):
                    g.SetVisible(False)
                    #module.GraphicalItems().Remove (g)
                else:
                    g.SetVisible(True)
                    fabrefdes=True

    if not fabrefdes:
        #Add text to module
        text = TEXTE_MODULE(module)
        p = module.GetPosition()
        px = p[0]
        py = p[1]
        layer = module.GetLayer()
        pos = wxPoint (px,py)
        text.SetPosition(pos)
        if layer == F_Cu:
            text.SetLayer(F_Fab)
        else:
            text.SetLayer(B_Fab)
        text.SetVisible (True)
        text.SetTextSize(wxSize (FromMM(0.5), FromMM(0.5)))
        text.SetThickness(FromMM(0.1))
        text.SetText("%R")
        module.Add(text)
Refresh()
board.Save("fabtmp.kicad_pcb")

pctl = PLOT_CONTROLLER(board)

popt = pctl.GetPlotOptions()

popt.SetOutputDirectory(plotDir)

# Set some important plot options:
popt.SetPlotFrameRef(False)
popt.SetLineWidth(FromMM(0.1))
popt.SetPlotReference(True)
popt.SetPlotValue(True)
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
plot_plan = [
    ( F_CrtYd,   "CrtYdTop",     "Courtyard Top"),
    ( F_Fab,     "FabricationTop",     "Fabrication Top" ),
    ( B_CrtYd,   "CrtYdBot",     "Courtyard Bottom" ),
    ( B_Fab,     "FabricationBot",     "Fabrication Bottom" ),
]
for layer_info in plot_plan:
    pctl.SetLayer(layer_info[0])
    pctl.OpenPlotfile(layer_info[1], PLOT_FORMAT_PDF, layer_info[2])
    pctl.PlotLayer()
    pctl.OpenPlotfile(layer_info[1], PLOT_FORMAT_GERBER, layer_info[2])
    pctl.PlotLayer()
# At the end you have to close the last plot, otherwise you don't know when
# the object will be recycled!
pctl.ClosePlot()
