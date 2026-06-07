# SPDX-FileCopyrightText: 2025 Karl Wette
#
# SPDX-License-Identifier: MIT

"""pre-commit hook to lint/format BibTeX bibliographies."""

import argparse
from typing import Sequence

from pybtex.database import parse_string

__author__ = "Karl Wette"


class ParseError(Exception):
    """Raise if BibTeX file could not be parsed."""


def main(argv: Sequence[str] | None = None) -> int:
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    for filename in args.filenames:

        # read BibTeX file
        comment_lines = []
        bibtex_lines = []
        with open(filename, "rt") as f:
            for line in f:
                line = line.strip()

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

        # make entries types all lowercase
        for entry in bib_data.entries.values():
            entry.original_type = entry.original_type.lower()

        # format BibTeX entries
        lines = []
        lines.extend(comment_lines)
        if bib_data.preamble:
            lines.extend(["", f'@preamble{{"{bib_data.preamble}"}}'])
        for entry in sorted(bib_data.entries.values(), key=lambda entry: entry.key):
            lines.extend(["", f"@{entry.original_type.lower()}{{{entry.key},"])
            entry_lines = []
            for field, people in entry.persons.items():
                people_strs = []
                for person in people:
                    person_str = ""
                    if len(person.prelast_names) > 0:
                        person_str += " " + " ".join(person.prelast_names)
                    person_str += " ".join(person.last_names)
                    if len(person.lineage_names) > 0:
                        person_str += ", " + " ".join(person.lineage_names)
                    person_str += ", " + " ".join(person.first_names)
                    if len(person.middle_names) > 0:
                        person_str += " " + " ".join(person.middle_names)
                    people_strs.append(person_str.strip())
                people_str = " and ".join(people_strs)
                if '"' in people_str:
                    entry_lines.append(f"    {field} = {{{people_str}}}")
                else:
                    entry_lines.append(f'    {field} = "{people_str}"')
            for field, value in entry.fields.items():
                if '"' in value:
                    entry_lines.append(f"    {field} = {{{value}}}")
                else:
                    entry_lines.append(f'    {field} = "{value}"')
            lines.append(",\n".join(entry_lines))
            lines.append("}")

        # output BibTeX entries
        while lines[0] == "":
            lines.pop(0)
        with open(filename, "wt") as f:
            for line in lines:
                print(line, file=f)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
