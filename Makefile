PYTHON = python3

all: dist/a.tsv dist/b.tsv dist/c.tsv dist/d.tsv dist/e.tsv

deps:
	pip install .

dist/%.tsv: data/%.tsv bin/gen.py deps
	mkdir -p dist
	$(PYTHON) bin/gen.py $< > $@
