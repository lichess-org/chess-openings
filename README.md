Chess opening names
===================

An aggregated data set of chess opening names.

field | `/` | `dist/` | description
--- | --- | --- | ---
eco | x | x | [ECO](https://en.wikipedia.org/wiki/Encyclopaedia_of_Chess_Openings) classification
name | x | x | Opening name (English language)
pgn | x | x| Well known sequence of moves, or the most common moves to reach the opening position based on master games, as PGN
uci | | x | Same moves as `pgn` in [UCI notation](https://backscattering.de/chess/uci/#move)
epd | | x | [EPD](https://www.chessprogramming.org/Extended_Position_Description) (FEN without move numbers) of the opening position, en passant field only if legal

Contributing
------------

Improvements, additions and fixes are welcome.

Regenerate the files in `dist/` by runnig `make`. Do not manually edit them.

Copyright
---------

As a collection of facts, this data set is in the public domain.
Considerable effort was spent curating and cleaning the data. Insofar as that
qualifies for copyright, the work is released under the
CC0 Public Domain Dedication.

[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
