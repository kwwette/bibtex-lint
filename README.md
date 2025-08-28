# bibtex-lint

[pre-commit] hook to lint/format [BibTeX] bibliographies. Uses [pybtex].

To use the hook, add the following to `.pre-commit-hooks.yaml`:

```
repos:
  - repo: https://github.com/kwwette/bibtex-lint.git
    rev: # see repository for latest tag
    hooks:
      - id: bibtex-lint
```

[pre-commit]:                   https://pre-commit.com/
[BibTeX]:                       https://www.bibtex.org/
[pybtex]:                       https://pybtex.org/
