#!/usr/bin/python3

import chess
import itertools
import sys


def main(arg, db):
    ret = 0
    prev_eco = ""
    prev_name = ""

    with open(arg) as f:
        for lno, line in zip(itertools.count(1), f):
            cols = line.rstrip("\n").split("\t")

            if len(cols) != 4:
                print(f"::error file={arg},line={lno}::expected 4 columns, got {len(cols)}")
                ret = 1
                continue

            if lno == 1:
                if cols != ["eco", "name", "fen", "moves"]:
                    print(f"::error file={arg},line={lno}::expected eco, name, fen, moves")
                    ret = 1
                continue

            eco, name, fen, moves = cols
            moves = moves.split(" ")

            if name.count(":") > 1:
                print(f"::warning file={arg},line={lno}::multiple ':' in name: {name}")

            if fen in db:
                print(f"::warning file={arg},line={lno}::duplicate fen: {db[fen]}")
            else:
                db[fen] = cols

            if eco < prev_eco:
                print(f"::warning file={arg},line={lno}::not ordered by eco ({eco} after {prev_eco})")
            elif (eco, name) < (prev_eco, prev_name):
                print(f"::warning file={arg},line={lno}::not ordered by name ({name!r} after {prev_name!r})")
            prev_eco = eco
            prev_name = name

            try:
                board = chess.Board()
                for move in moves:
                    board.push_uci(move)
                if fen != board.epd():
                    print(f"::error file={arg},line={lno}::mismatching fen, expected: {board.fen()}")
                    ret = 1
            except ValueError as err:
                print(f"::error file={arg},line={lno}::{err}")
                ret = 1

            for blacklisted in ["refused"]:
                if blacklisted in name.lower():
                    print(f"::warning file={arg},line={lno}::blacklisted word ({blacklisted!r} in {name!r})")

    return ret


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} *.tsv")
        sys.exit(2)

    db = {}
    ret = 0
    for arg in sys.argv[1:]:
        ret = max(ret, main(arg, db))
    sys.exit(ret)
