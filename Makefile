PYTHON = python3

OUTPUT_OPENINGS = dist/a.tsv dist/b.tsv dist/c.tsv dist/d.tsv dist/e.tsv
INPUT_OPENINGS = data/a.tsv data/b.tsv data/c.tsv data/d.tsv data/e.tsv
OUTPUT_ALL = dist/all.tsv

all: deps $(OUTPUT_OPENINGS) $(OUTPUT_ALL)

deps:
	pip install .

$(OUTPUT_ALL):
	$(PYTHON) bin/gen.py $(INPUT_OPENINGS) > $@

dist/%.tsv: $(INPUT_OPENINGS) bin/gen.py
	mkdir -p dist
	$(PYTHON) bin/gen.py $< > $@

clean:
	rm $(OUTPUT_OPENINGS) $(OUTPUT_ALL)
