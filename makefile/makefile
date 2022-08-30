# -*- Makefile -*-
# linux only

SCRIPTPATH = /media/sf_uie24052/repositories/kicad-tools/
TEMPLATEPATH = /media/sf_uie24052/repositories/gerbv-tools/

PROJECT = LTE_MR_6.1.0

all: gerbers drill stackup pnp schpdf bom assypdf laypdf gerbvproj

schpdf: $(PROJECT).kicad_sch
	@mkdir -p outputs
	#$(foreach variant,$(VARIANTS),python3 $(SCRIPTPATH)schematic_variant.py $< outputs/)
	python3 $(SCRIPTPATH)eeschema-tools/schpdf.py $<

gerbers: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	#No Reference Designators
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-gerb.py $< outputs/gerbers/ -r false

drill: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/drill
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-drill.py $< outputs/drill/

laypdf: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-gerb.py -f pdf $< outputs/gerbers/

gerbvproj: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/gerbers
	cp $(TEMPLATEPATH)template-6L.gvp outputs/gerbers/$(PROJECT).gvp
	sed -i 's+project+$(PROJECT)+g' outputs/gerbers/$(PROJECT).gvp
	sed -i 's+path+$(dir $(abspath $(lastword $(MAKEFILE_LIST))))+g' outputs/gerbers/$(PROJECT).gvp

pnp: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/pnp
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-pnp.py $< outputs/pnp/

assypdf: $(PROJECT).kicad_pcb
	@mkdir -p outputs
	@mkdir -p outputs/pnp
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-assypdf.py $< outputs/pnp/
	pdftk outputs/pnp/$(PROJECT)-FabricationBot.pdf background outputs/pnp/$(PROJECT)-CrtYdBot.pdf output outputs/pnp/$(PROJECT)-AssyBot.pdf
	pdftk outputs/pnp/$(PROJECT)-FabricationTop.pdf background outputs/pnp/$(PROJECT)-CrtYdTop.pdf output outputs/pnp/$(PROJECT)-AssyTop.pdf
	rm outputs/pnp/$(PROJECT)-FabricationBot.pdf outputs/pnp/$(PROJECT)-CrtYdBot.pdf outputs/pnp/$(PROJECT)-FabricationTop.pdf outputs/pnp/$(PROJECT)-CrtYdTop.pdf
	gerbv outputs/pnp/$(PROJECT)-FabricationTop.gbr outputs/pnp/$(PROJECT)-CrtYdTop.gbr -x rs274x -o outputs/pnp/$(PROJECT)-AssyTop.gbr
	gerbv outputs/pnp/$(PROJECT)-FabricationBot.gbr outputs/pnp/$(PROJECT)-CrtYdBot.gbr -x rs274x -o outputs/pnp/$(PROJECT)-AssyBot.gbr
	rm outputs/pnp/$(PROJECT)-FabricationBot.gbr outputs/pnp/$(PROJECT)-CrtYdBot.gbr outputs/pnp/$(PROJECT)-FabricationTop.gbr outputs/pnp/$(PROJECT)-CrtYdTop.gbr
	rm fabtmp.kicad_pcb
	rm fabtmp.kicad_pro
	rm fabtmp.kicad_prl

clean:
	rm fabtmp.kicad_pcb
	rm fabtmp.kicad_pro
	rm fabtmp.kicad_prl
	rm -rf outputs/

#TODO
stackup: TD4PCB.xlsx
	@mkdir -p outputs
	soffice --headless --convert-to pdf:calc_pdf_Export --outdir outputs $<
	pdftk outputs/TD4PCB_PCB.pdf cat 2 output outputs/TD4PCB_PCB.pdf
	#python3 $(STACKUPPATH)kicad-stackup-editor --pcb $< --out outputs/$(PROJECT).pdf

fabzip: gerbers drill pnp assypdf stackup
	zip -r outputs/$(PROJECT)_fab.zip outputs/pnp/ outputs/gerbers/ outputs/drill TD4PCB_PCB.pdf

bom: $(PROJECT).kicad_sch
	@mkdir -p outputs
	python3 $(SCRIPTPATH)eeschema-tools/schbom.py $<
	python3 $(SCRIPTPATH)/bom_csv_conti_sorted_by_ref.py $(PROJECT).xml $(PROJECT).csv

3dmodel: $(PROJECT).kicad_pcb
	python3 $(SCRIPTPATH)pcbnew-tools/kicad-assy.py $< outputs/pnp/

zip: fabzip bom schpdf 3dmodel
	zip -r outputs/$(PROJECT).zip outputs/
