#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import collections
import logging
import copy
import sys

import chess
import chess.pgn

db = {}

for line in open("eco.json", "r"):
    line = line.replace("db.eco.insert(", "").replace(");,", "")
    record = json.loads(line)
    db[record["f"]] = record

pgn_file = open("masters.pgn", "r", errors="surrogateescape")

class Visitor(chess.pgn.BaseVisitor):
    def __init__(self):
        self.found_game = False
        self.moves = None

    def begin_game(self):
        self.found_game = True

    def visit_move(self, board, move):
        fen = " ".join([board.board_fen(), "w" if board.turn == chess.WHITE else "b", board.castling_xfen()])
        if fen in db:
            if "m" not in db[fen]:
                db[fen]["m"] = collections.defaultdict(lambda: 0)

            db[fen]["m"][self.moves] += 1

        self.moves = self.moves + " " + board.uci(move) if self.moves else board.uci(move)

    def handle_error(self, error):
        logging.exception("error during pgn parsing")

    def result(self):
        return self.found_game

def num_matched(db):
    return sum(1 for record in db.values() if "m" in record)

logging.basicConfig(level=logging.INFO)

more_work = True
i = 0
while more_work:
    more_work = chess.pgn.read_game(pgn_file, Visitor)

    i += 1

    if i % 50 == 0:
        matched = num_matched(db)
        print("%i | %d / %d = %.03f" % (i, matched, len(db), matched / len(db)), file=sys.stderr)

    if i % 5000 == 0:
        result_file = open("result.%d.json" % i, "w")

        for r in db.values():
            record = copy.deepcopy(r)
            try:
                m = max(record["m"], key=lambda k: record["m"][k])
            except (ValueError, KeyError):
                m = "XXX"

            record["m"] = m

            print(json.dumps(record), file=result_file)
            print(json.dumps(record))

        result_file.close()
