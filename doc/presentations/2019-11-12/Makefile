PDF=presentation.pdf
TEXFILE=main

all: $(TEXFILE).tex
	./latexrun --latex-args="-shell-escape --output-directory=latex.out/" $(TEXFILE).tex && mv $(TEXFILE).pdf $(PDF)

view: $(PDF)
	xdg-open $(PDF) &

# Clean up stray files
clean:
	rm -fv $(OUT_FILES)
	rm -rf latex.out
	rm -fv $(PDF)
