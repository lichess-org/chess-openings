#!/usr/bin/python3

import chess.pgn
import sys
import io
import itertools
import glob
import os
import json

def main(argv):
    files = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist")) + os.path.sep + "*.tsv")
    openings = []

    for f in files:
        for line in itertools.islice(open(f), 1, None):
            eco, name, pgn, uci, epd = map(str.strip, line.split("\t"))
            openings.append({
                'name': name,
                'eco': eco,
                'pgn': pgn,
                'uci': uci,
                'epd': epd
            })
        
    print(json.dumps(openings))

if __name__ == "__main__":
    main(sys.argv)
