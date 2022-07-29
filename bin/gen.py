#!/usr/bin/python3

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


def main(arg, by_epd, shortest_by_name):
    ret = 0
    prev_eco = ""
    prev_name = ""

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

            if shortest_by_name.get(name, -1) == len(board.move_stack):
                print(f"::warning file={arg},line={lno}::{name!r} does not have a unique shortest line", file=sys.stderr)
            try:
                shortest_by_name[name] = min(shortest_by_name[name], len(board.move_stack))
            except KeyError:
                shortest_by_name[name] = len(board.move_stack)

            clean_pgn = chess.Board().variation_san(board.move_stack)
            if clean_pgn != pgn:
                print(f"::warning file={arg},line={lno}::unclean pgn: expected {clean_pgn!r}, got {pgn!r}", file=sys.stderr)

            if name.count(":") > 1:
                print(f"::warning file={arg},line={lno}::multiple ':' in name: {name}", file=sys.stderr)

            for blacklisted in ["refused"]:
                if blacklisted in name.lower():
                    print(f"::warning file={arg},line={lno}::blacklisted word ({blacklisted!r} in {name!r})", file=sys.stderr)

            epd = board.epd()
            if epd in by_epd:
                print(f"::warning file={arg},line={lno}::duplicate epd: {by_epd[epd]}", file=sys.stderr)
            else:
                by_epd[epd] = cols

            if eco < prev_eco:
                print(f"::warning file={arg},line={lno}::not ordered by eco ({eco} after {prev_eco})", file=sys.stderr)
            elif (eco, name) < (prev_eco, prev_name):
                print(f"::warning file={arg},line={lno}::not ordered by name ({name!r} after {prev_name!r})", file=sys.stderr)
            prev_eco = eco
            prev_name = name

            print(eco, name, clean_pgn, " ".join(m.uci() for m in board.move_stack), epd, sep="\t")

    return ret


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} *.tsv", file=sys.stderr)
        sys.exit(2)

    print("eco", "name", "pgn", "uci", "epd", sep="\t")

    by_epd = {}
    shortest_by_name = {}
    ret = 0
    for arg in sys.argv[1:]:
        ret = max(ret, main(arg, by_epd, shortest_by_name))
    sys.exit(ret)
