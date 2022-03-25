FLAGS1= --metadata link-citations -F pandoc-citeproc --csl=elsevier-with-titles.csl --bibliography=manual.bib --toc
FLAGS2= --mathjax -V colorlinks=true -V linkcolor=blue -V urlcolor=red -V toccolor=gray
FLAGS3= -V mainfont=IPAMincho -V classoption=onecolumn --pdf-engine=lualatex -V documentclass=ltjarticle -V geometry:margin=1in
FLAGS=$(FLAGS1) $(FLAGS2) $(FLAGS3)
OBJ=manual.pdf manual_jp.pdf tutorial_jp.pdf

all:$(OBJ)

%.pdf : %.md
	pandoc $(FLAGS) $< -o $@

clean:
	rm manual.pdf manual_jp.pdf tutorial_jp.pdf
