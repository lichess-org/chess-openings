#!/usr/bin/python3
#
# Generate one PGN file from the tsv files. Just a simple mod of gen.py.

import io
import itertools
import sys

try:
    import chess
    import chess.pgn
except ImportError:
    print("Need python-chess:", file=sys.stderr)
    print("$ pip3 install chess", file=sys.stderr)
    print(file=sys.stderr)
    raise

files = ["../a.tsv", "../b.tsv", "../c.tsv", "../d.tsv", "../e.tsv"]

db = {}
prev_eco = ""
prev_name = ""
outfile = open("../dist/eco.pgn", "w")
for arg in files:
    with open(arg) as f:
        for lno, line in zip(itertools.count(1), f):
            cols = line.rstrip("\n").split("\t")

            if len(cols) != 3:
                print(f"::error file={arg},line={lno}::expected 3 columns, got {len(cols)}", file=sys.stderr)
                ret = 1
                continue

            if lno == 1:
                if cols != ["eco", "name", "pgn"]:
                    print(f"::error file={arg},line={lno}::expected eco, name, pgn", file=sys.stderr)
                    ret = 1
                continue

            eco, name, pgn = cols

            try:
                board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
            except ValueError as err:
                print(f"::error file={arg},line={lno}::{err}", file=sys.stderr)
                ret = 1
                continue

            clean_pgn = chess.Board().variation_san(board.move_stack)
            if clean_pgn != pgn:
                print(f"::warning file={arg},line={lno}::unclean pgn: expected {clean_pgn!r}, got {pgn!r}", file=sys.stderr)

            if name.count(":") > 1:
                print(f"::warning file={arg},line={lno}::multiple ':' in name: {name}", file=sys.stderr)

            for blacklisted in ["refused"]:
                if blacklisted in name.lower():
                    print(f"::warning file={arg},line={lno}::blacklisted word ({blacklisted!r} in {name!r})", file=sys.stderr)

            epd = board.epd()
            if epd in db:
                print(f"::warning file={arg},line={lno}::duplicate epd: {db[epd]}", file=sys.stderr)
            else:
                db[epd] = cols

            if eco < prev_eco:
                print(f"::warning file={arg},line={lno}::not ordered by eco ({eco} after {prev_eco})", file=sys.stderr)
            elif (eco, name) < (prev_eco, prev_name):
                print(f"::warning file={arg},line={lno}::not ordered by name ({name!r} after {prev_name!r})", file=sys.stderr)
            prev_eco = eco
            prev_name = name

            #print(eco, name, clean_pgn, " ".join(m.uci() for m in board.move_stack), epd, sep="\t")

            game = chess.pgn.Game().from_board(board)
            name = name.split(": ")
            game.headers["White"] = name[0]
            if len(name) > 1:
                game.headers["Black"] = name[1]
            game.headers["ECO"] = eco

            print(game, file=outfile, end="\n\n")

outfile.close()
