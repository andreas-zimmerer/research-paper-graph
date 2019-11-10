PDF=presentation.pdf
TEXFILE=main
PLOT_PREFIX=ggplot_example_

RFILES := $(wildcard R/*.R)

PLOT_FILES := $(wildcard R/$(PLOT_PREFIX)*.R)
OUT_FILES:= $(PLOT_FILES:.R=.Rout)
PDF_ENDING:= $(PLOT_FILES:.R=.pdf)
PDF_PLOTS = $(subst $(PLOT_PREFIX),,$(PDF_ENDING))


all: $(OUT_FILES) $(PDF)

$(PDF): $(TEXFILE).tex $(OUT_FILES)
	./latexrun --latex-args="-shell-escape --output-directory=latex.out/" $(TEXFILE).tex && mv $(TEXFILE).pdf $(PDF)

R/%.Rout: R/%.R
	cd R && Rscript ../$< && R CMD BATCH ../$<

Plots: $(OUT_FILES)

view: $(PDF)
	xdg-open $(PDF) &

# Clean up stray files
clean:
	rm -fv $(OUT_FILES)
	rm -fv $(PDF_PLOTS)
	rm -rf latex.out
	rm -fv $(PDF)

printPlotNames:
	echo $(PDF_PLOTS)
