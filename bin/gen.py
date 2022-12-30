#!/usr/bin/python3

import io
import re
import sys

from typing import Dict, List, TextIO

try:
    import chess
    import chess.pgn
except ImportError:
    print("Need python-chess:", file=sys.stderr)
    print("$ pip3 install chess", file=sys.stderr)
    print(file=sys.stderr)
    raise


ECO_REGEX = re.compile(r"^[A-E]\d\d\Z")

INVALID_SPACE = re.compile(r"\s{2,}|^\s|\s\Z|\s,")

INVALID_WITH = re.compile(r"[^,:]\swith\b")


class Stats:
    def __init__(self) -> None:
        self.errors = 0
        self.warnings = 0

class Reporter:
    def __init__(self, stats: Stats, file_name: str) -> None:
        self.stats = stats
        self.file_name = file_name

    def error(self, lno: int, err_msg: str) -> None:
        print(f"::error file={self.file_name},line={lno}::{err_msg}", file=sys.stderr)
        self.stats.errors += 1

    def warning(self, lno: int, err_msg: str) -> None:
        print(f"::warning file={self.file_name},line={lno}::{err_msg}", file=sys.stderr)
        self.stats.warnings += 1


def main(f: TextIO, reporter: Reporter, by_epd: Dict[str, List[str]], shortest_by_name: Dict[str, int]) -> None:
    prev_eco = ""
    prev_name = ""

    for lno, line in enumerate(f, 1):
        cols = line.rstrip("\n").split("\t")

        if len(cols) != 3:
            reporter.error(lno, f"expected 3 columns, got {len(cols)}")
            continue

        if lno == 1:
            if cols != ["eco", "name", "pgn"]:
                reporter.error(lno, f"expected eco, name, pgn")
            continue

        eco, name, pgn = cols

        if not ECO_REGEX.match(eco):
            reporter.error(lno, f"invalid eco")
            continue

        if INVALID_SPACE.search(name):
            reporter.error(lno, f"invalid whitespace in name")
            continue

        try:
            board = chess.pgn.read_game(io.StringIO(pgn), Visitor=chess.pgn.BoardBuilder)
        except ValueError as err:
            reporter.error(lno, f"{err}")
            continue

        if not board:
            reporter.error(lno, f"Empty pgn")
            continue

        allowed_lowers = ["with", "de", "der", "del", "von", "and"]
        if not all([word[0].isupper() for word in re.split(r"\s|-", name) if word not in allowed_lowers and word.isalpha()]):
            reporter.warning(lno, f"{name!r} word(s) beginning with lowercase letters")

        if INVALID_WITH.search(name):
            reporter.warning(lno, f"'with' not separated with ',' or ':'")

        for blacklisted in ["refused"]:
            if blacklisted in name.lower():
                reporter.warning(lno, f"blacklisted word ({blacklisted!r} in {name!r})")


        if shortest_by_name.get(name, -1) == len(board.move_stack):
            reporter.warning(lno, f"{name!r} does not have a unique shortest line")
        try:
            shortest_by_name[name] = min(shortest_by_name[name], len(board.move_stack))
        except KeyError:
            shortest_by_name[name] = len(board.move_stack)

        clean_pgn = chess.Board().variation_san(board.move_stack)
        if clean_pgn != pgn:
            reporter.error(lno, f"unclean pgn: expected {clean_pgn!r}, got {pgn!r}")

        if name.count(":") > 1:
            reporter.error(lno, f"multiple ':' in name: {name}")

        epd = board.epd()
        if epd in by_epd:
            reporter.error(lno, f"duplicate epd: {by_epd[epd]}")
        else:
            by_epd[epd] = cols

        if eco < prev_eco:
            reporter.error(lno, f"not ordered by eco ({eco} after {prev_eco})")
        elif (eco, name) < (prev_eco, prev_name):
            reporter.error(lno, f"not ordered by name ({name!r} after {prev_name!r})")
        prev_eco = eco
        prev_name = name

        print(eco, name, clean_pgn, " ".join(m.uci() for m in board.move_stack), epd, sep="\t")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} *.tsv", file=sys.stderr)
        sys.exit(2)

    print("eco", "name", "pgn", "uci", "epd", sep="\t")

    stats = Stats()
    by_epd: Dict[str, List[str]] = {}
    shortest_by_name: Dict[str, int] = {}
    for file_name in sys.argv[1:]:
        with open(file_name) as f:
            main(f, Reporter(stats, file_name), by_epd, shortest_by_name)
    if stats.errors:
        sys.exit(1)
