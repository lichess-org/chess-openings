PYTHON := $(shell command -v python3 || command -v python)

all: dist/a.tsv dist/b.tsv dist/c.tsv dist/d.tsv dist/e.tsv

dist/%.tsv: %.tsv bin/gen.py
	mkdir -p dist
	$(PYTHON) bin/gen.py $< > $@
