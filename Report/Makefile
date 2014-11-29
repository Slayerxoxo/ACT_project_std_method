all: main tableofcontents 

main: main.tex
	pdflatex main.tex
	
biblio: biblio.bib main.tex
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

tableofcontents: main.tex
	pdflatex main.tex

clean:
	rm *.aux *.toc *.log *.out 
	
clean_biblio:
	rm *.aux *.toc *.log *.out *.bbl *.blg
