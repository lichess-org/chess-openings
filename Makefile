PYTHON = python3

all: dist/a.tsv dist/b.tsv dist/c.tsv dist/d.tsv dist/e.tsv

dist/%.tsv: %.tsv bin/gen.py
	$(PYTHON) bin/gen.py $< > $@
