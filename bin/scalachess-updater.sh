#!/bin/sh

scalachess_path=~/scalachess

for l in a b c d e; do ./bin/to-scalachess.py dist/$l.tsv > $scalachess_path/src/main/scala/opening/FullOpeningPart${l^}.scala; done
