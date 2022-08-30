#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Ungrouped (One component per row) CSV output
#

"""
    @package
    Output: CSV (comma-separated)
    Grouped By: ungrouped, one component per line
    Sorted By: Ref
    Fields: Ref, Value, Part, Footprint, Datasheet, Manufacturer, Vendor

    Command line:
    python "pathToFile/bom_csv_sorted_by_ref.py" "%I" "%O.csv"
"""

from __future__ import print_function

# Import the KiCad python helper module
import kicad_netlist_reader
import kicad_utils
import csv
import sys
from pcbnew import *

# A helper function to convert a UTF8/Unicode/locale string read in netlist
# for python2 or python3
def fromNetlistText( aText ):
    if sys.platform.startswith('win32'):
        try:
            return aText.encode('utf-8').decode('cp1252')
        except UnicodeDecodeError:
            return aText
    else:
        return aText

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = kicad_utils.open_file_write(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout
# Assembly Part List incl. Component Properties
#
# Date = 2022/06/02 13:49:48
# Job Name =C:\CAx\Prj\ZUKEN\41710752_AC_RCK_Gen2.1\job\bd\job.dsgn
# Units = millimeters
# Decimal Digits =3
#
# PCB/PNL Type;Offset-X;Offset-Y;Rotation
#
# NA;0.000;0.000;0.000
#

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=';')

# override csv.writer's writerow() to support utf8 encoding:
def writerow( acsvwriter, columns ):
    utf8row = []
    for col in columns:
        utf8row.append( fromNetlistText( str(col) ) )
    acsvwriter.writerow( utf8row )

components = net.getInterestingComponents()

# Output a field delimited header line
writerow( out, ['# Assembly Part List incl. Component Properties'])
writerow( out, ['#'])
#writerow( out, ['Date:', net.getDate()] )
writerow( out, ['# Date = '+ net.getDate()] )
#writerow( out, ['Source:', net.getSource()] )
writerow( out, ['# Job Name = '+ net.getSource()] )
writerow( out, ['# Units = millimeters'])
#writerow( out, ['Tool:', net.getTool()] )
#writerow( out, ['Component Count:', len(components)] )
writerow( out, ['# Decimal Digits =3'])
writerow( out, ['#'])
writerow( out, ['# PCB/PNL Type;Offset-X;Offset-Y;Rotation'])
writerow( out, ['#'])
writerow( out, ['# NA;0.000;0.000;0.000'])
writerow( out, ['#'])

#writerow( out, ['Ref', 'Value', 'Footprint', 'Datasheet', 'Manufacturer', 'Vendor'] )
writerow( out, ['# Reference','Part_Name','Value','Tolerance','Pos_Tolerance','Neg_Tolerance','Geometry','Rated_Voltage','Technology','Placement_Side','Rotation','Position-X','Positon-Y','Pin_Count','Component_Height_on_Placement_Side','Part_Families','Mounting_Type','Footprint_Specification','Package_Type','Function_Code','EMC_Code','Board# on Panel','Part_Name_SV','Part_Name_CAS','Exclude_from_SAP_BOM','Multipitch_Pair','Nomenclature', 'Supplier Name', 'Supplier Part Name'])

pcb = LoadBoard('.'.join(sys.argv[1].split('.')[:-1])+'.kicad_pcb')
side = {"True":"B_SIDE", "False":"A_SIDE"}
attributes = {1:"THT", 2:"SURFACE", 12:"UNDEF"}

# Output all of the component information (One component per row)
for c in components:
    for m in pcb.GetFootprints():
        if m.GetReference()==c.getRef():
            coordinates = (format((m.GetCenter()[0])/1000.0/1000.0,".3f"), format((m.GetCenter()[1])/1000.0/1000.0,".3f"))
            rot = int(m.GetOrientationDegrees())
            if (rot<0):
                rot = rot+360
            rot = format(rot,".3f")
            break
    if (c.getValue()=="NC"):
            a2c = "NC"
    else:
        if (c.getField("A2C")==""):
            #writerow( out, [c.getRef(),"NA", c.getValue(),'','','', c.getFootprint(),'','',side[str(m.IsFlipped())],rot,coordinates[0],coordinates[1],'','','',attributes[m.GetAttributes()],'','','','','','','','','',c.getField("Description"), c.getField("Manufacturer"), c.getField("MPN")])
            a2c = "NA"
        else:
            a2c = c.getField("A2C")
    writerow( out, [c.getRef(), a2c, c.getValue(),'','','', c.getFootprint(),'',attributes[m.GetAttributes()],side[str(m.IsFlipped())],rot,coordinates[0],coordinates[1],'','','',attributes[m.GetAttributes()],'','','','','',c.getField("A2C"),c.getField("A2C"),'','',c.getField("Description"), c.getField("Manufacturer"), c.getField("MPN")])
#    ,,, c.getDatasheet(), c.getField("Manufacturer"), c.getField("Vendor")])
