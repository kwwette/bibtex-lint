# SPDX-FileCopyrightText: 2025 Karl Wette
#
# SPDX-License-Identifier: MIT

"""pre-commit hook to lint/format BibTeX bibliographies."""

import argparse
from typing import Sequence

from pybtex.database import BibliographyData, parse_string

__author__ = "Karl Wette"


class ParseError(Exception):
    """Raise if BibTeX file could not be parsed."""


def main(argv: Sequence[str] | None = None) -> int:
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    for filename in args.filenames:

        # read BibTeX file
        comment_lines = []
        bibtex_lines = []
        with open(filename, "rt") as f:
            for line in f:
                line = line.lstrip()

                # save comment lines
                if line.startswith("%"):
                    comment_lines.append(line)

                # add all lines to BibTeX, to preserve line numbers when parsing
                bibtex_lines.append(line)

        # parse BibTeX entries
        bibtex_string = "".join(bibtex_lines)
        try:
            bib_data = parse_string(bibtex_string, "bibtex")
        except Exception:
            msg = f"could not parse BibTeX file {filename}"
            raise ParseError(msg)

        # sort BibTeX entries
        sorted_bib_data = BibliographyData(
            entries=dict(sorted(bib_data.entries.items())), preamble=bib_data.preamble
        )

        # format and output BibTeX entries
        with open(filename, "wt") as f:
            for line in comment_lines:
                f.write(line)
            f.write("\n")
            f.write(sorted_bib_data.to_string("bibtex"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
