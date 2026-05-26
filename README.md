Chess opening names
===================

An aggregated data set of chess opening names.

field | `/` | `dist/` | description
--- | --- | --- | ---
eco | x | x | [ECO](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings) classification
name | x | x | Opening name (English language)
pgn | x | x | Well-known sequence of moves, or the most common moves to reach the opening position based on master games, as PGN
uci | | x | Same moves as `pgn` in [UCI notation](https://backscattering.de/chess/uci/#move)
epd | | x | [EPD](https://www.chessprogramming.org/Extended_Position_Description) (FEN without move numbers) of the opening position, en passant field only if legal

To generate `dist/`, install Python, then run `pip3 install chess` and `make`.
Or select the latest
[workflow run](https://github.com/lichess-org/chess-openings/actions) and
download build artifacts.

This dataset is also [available in the Apache Parquet format](https://hf.co/datasets/Lichess/chess-openings).

Conventions
-----------

* Title case is used for opening names.
* Names are structured like `Opening family: Variation, Subvariation, ...`,
  e.g., `Sicilian Defense: Najdorf Variation, English Attack`.
* The suggested way to classify games is to traverse moves backwards until
  a named position is found. To make this work well with common transpositions,
  multiple entries for a single opening may be added.
* However, each name has a unique *shortest* line. If necessary,

Opening data is in `a.tsv`, `b.tsv`, `c.tsv`, `d.tsv`, and `e.tsv`, with the filenames corresponding to [ECO volumes](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings#Openings_covered).

Improvements, additions, and fixes are welcome. If you have concrete
suggestions, please be bold and submit the proposed changes directly as pull
requests!
