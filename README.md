# assorted-pre-commit-hooks / bibtex

[pre-commit] hook to lint/format [BibTeX] bibliographies. Uses [pybtex].

To use the hook, add the following to `.pre-commit-hooks.yaml`:

```
repos:
  - repo: https://github.com/assorted-pre-commit-hooks/bibtex
    rev: # see repository for latest tag
    hooks:
      - id: bibtex
```

[pre-commit]:   https://pre-commit.com/
[BibTeX]:       https://www.bibtex.org/
[pybtex]:       https://pybtex.org/
