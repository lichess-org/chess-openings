PYTHON = python3

sources = a.tsv b.tsv c.tsv d.tsv e.tsv

all: dist/all.tsv $(sources:%=dist/%)

dist/all.tsv: $(sources) bin/gen.py
	mkdir -p dist
	$(PYTHON) bin/gen.py $(sources) > $@

dist/%.tsv: %.tsv bin/gen.py
	mkdir -p dist
	$(PYTHON) bin/gen.py $< > $@

.PHONY: clean
clean:
	rm -f dist/all.tsv $(sources:%=dist/%)
