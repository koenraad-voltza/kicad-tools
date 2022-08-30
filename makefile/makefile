# -*- Makefile -*-
# Based on https://github.com/hzeller/ldgraphy/tree/master/pcb/kicad-scripts
# Added symlink and ability to run from other tree depths

SCRIPTPATH = /home/voltza/repositories/voltza-github/tools/kicad-tools/makefile/
SCRIPTPATH2 = /home/voltza/repositories/voltza-github/tools/kicad-tools/
SCRIPTPATH3 = /home/voltza/repositories/voltza-github/tools/gerbv-tools/
STACKUPPATH = /home/voltza/repositories/misc-github/kicad_stackup_editor/
PROJECT = rck3-proto

#TODO: make sure output folder exists
all: gerbers gerbvproj drill stackup pnp bom schpdf assypdf laypdf

gerbers: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	python3 $(SCRIPTPATH)kicad-gerb.py $< outputs/gerbers/

gerbvproj: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	cp $(SCRIPTPATH3)template-2L.gvp outputs/gerbers/$(PROJECT).gvp
	sed -i 's/project/$(PROJECT)/g' outputs/gerbers/$(PROJECT).gvp
	sed -i 's+path+$(dir $(abspath $(lastword $(MAKEFILE_LIST))))+g' outputs/gerbers/$(PROJECT).gvp

drill: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/drill
	python3 $(SCRIPTPATH)kicad-drill.py $< outputs/drill/

pnp: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/pnp
	python3 $(SCRIPTPATH2)pos_tht.py $< outputs/pnp/

stackup: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	python3 $(STACKUPPATH)kicad-stackup-editor --pcb $< --out outputs/$(PROJECT).pdf

schpdf: $(PROJECT).sch
	@mkdir -p outputs
	#os.chdir("/home/voltza/repositories/voltza-github/tools/kicad-tools/") #TODO fixme
	PYTHONPATH=/home/voltza/repositories/voltza-github/tools/kicad-tools/ python -m eeschema.schematic export -f pdf -a $(PROJECT).sch outputs/
	rm outputs/export_schematic_screencast.ogv

bom: $(PROJECT).sch
	@mkdir -p outputs
	python3 $(SCRIPTPATH2)export_bom.py $< outputs/

assypdf: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/pnp
	python3 $(SCRIPTPATH)kicad-assypdf.py $< outputs/pnp/
	pdftk outputs/pnp/$(PROJECT)-FabricationBot.pdf background outputs/pnp/$(PROJECT)-CrtYdBot.pdf output outputs/pnp/$(PROJECT)-AssyBot.pdf
	pdftk outputs/pnp/$(PROJECT)-FabricationTop.pdf background outputs/pnp/$(PROJECT)-CrtYdTop.pdf output outputs/pnp/$(PROJECT)-AssyTop.pdf
	rm outputs/pnp/$(PROJECT)-FabricationBot.pdf outputs/pnp/$(PROJECT)-CrtYdBot.pdf outputs/pnp/$(PROJECT)-FabricationTop.pdf outputs/pnp/$(PROJECT)-CrtYdTop.pdf
	gerbv outputs/pnp/$(PROJECT)-FabricationTop.gbr outputs/pnp/$(PROJECT)-CrtYdTop.gbr -x rs274x -o outputs/pnp/$(PROJECT)-AssyTop.gbr
	gerbv outputs/pnp/$(PROJECT)-FabricationBot.gbr outputs/pnp/$(PROJECT)-CrtYdBot.gbr -x rs274x -o outputs/pnp/$(PROJECT)-AssyBot.gbr
	rm outputs/pnp/$(PROJECT)-FabricationBot.gbr outputs/pnp/$(PROJECT)-CrtYdBot.gbr outputs/pnp/$(PROJECT)-FabricationTop.gbr outputs/pnp/$(PROJECT)-CrtYdTop.gbr

laypdf: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	python3 $(SCRIPTPATH)kicad-gerb.py -f pdf $< outputs/gerbers/
	pdftk outputs/gerbers/$(PROJECT)-CuTop.pdf outputs/gerbers/$(PROJECT)-CuBottom.pdf outputs/gerbers/$(PROJECT)-Edge_Cuts.pdf outputs/gerbers/$(PROJECT)-SilkTop.pdf outputs/gerbers/$(PROJECT)-SilkBottom.pdf outputs/gerbers/$(PROJECT)-MaskTop.pdf outputs/gerbers/$(PROJECT)-MaskBottom.pdf outputs/gerbers/$(PROJECT)-PasteTop.pdf outputs/gerbers/$(PROJECT)-PasteBottom.pdf cat output outputs/gerbers/$(PROJECT).pdf #TODO: #layers>2
	rm outputs/gerbers/$(PROJECT)-CuTop.pdf outputs/gerbers/$(PROJECT)-CuBottom.pdf outputs/gerbers/$(PROJECT)-Edge_Cuts.pdf outputs/gerbers/$(PROJECT)-SilkTop.pdf outputs/gerbers/$(PROJECT)-SilkBottom.pdf outputs/gerbers/$(PROJECT)-MaskTop.pdf outputs/gerbers/$(PROJECT)-MaskBottom.pdf outputs/gerbers/$(PROJECT)-PasteTop.pdf outputs/gerbers/$(PROJECT)-PasteBottom.pdf

#TODO
3dmodel: $(PROJECT).kicad_pcb
	python3 $(SCRIPTPATH)kicad-assy.py $< outputs/pnp/

zip: fab-zip bom schpdf
	zip -r $@ $*_fab/

fab-zip: gerbers drill pnp stackup assypdf laypdf
	zip -r $@ $*_fab/

#%-fab.zip : %-fab.kicad_pcb
#	python $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))/kicad-fab.py $< plot/
	# Lines that start with '%TF' are "Gerber extensions" and are not
	# supported by some software (including the one that allpcb uses).
	# Be sure to test with both gerbv and gerbview for compatibility problems in
	# the future.
#	sed -i '/^%TF/d' plot/*
	# Include a unique directory name so you can unzip lots of these at the
	# same path.
#	[ -e $*_fab ] || ln -sf plot $*_fab
#	zip -r $@ $*_fab/

#clean:
#	rm -rf $(FABS) $(FABS:.zip=)
