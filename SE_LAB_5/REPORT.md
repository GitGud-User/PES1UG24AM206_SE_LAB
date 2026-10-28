# Lab 5: Static Code Analysis â€“ School Bus Transport Register

**SRN:** PES1UG24AM206
**Source repo:** https://github.com/SETAPESU26/L5_24_school_transport
**File analysed:** `school_transport.py`
**Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python 3.12, virtual environment)

## Folder contents

| Path | Contents |
|------|----------|
| `school_transport.py` | Updated, cleaned source file |
| `reports/before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` on the original file |
| `reports/after/` | The same three reports on the fixed file |
| `issues.md` | Issue table (issue, type, lines, description, fix) |
| `reflection.md` | Answers to the reflection questions |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | **4.00/10** (18 messages) | **10.00/10** (0 messages) |
| Bandit | 4 issues: 1 High, 1 Medium, 2 Low | **No issues identified** |
| Flake8 | 9 violations (E501 Ã—4, E231 Ã—3, E302, E722) | **0 violations** (empty report) |

## Commits

One commit per tool, in the order of priority (security first):

1. **Fix Bandit issues** â€“ parameterised SQL (B608), removed `subprocess.run(shell=True)` and the `subprocess` import (B602, B404), replaced `assert` with an explicit check (B101).
2. **Fix Pylint issues** â€“ docstrings (C0114/C0116), snake_case names (C0103), removed unused `driver` argument (W0613), `with open(..., encoding="utf-8")` (R1732/W1514), `except sqlite3.Error` instead of bare `except` (W0702), wrapped lines over 100 chars (C0301), plus `__main__` guard and `None` â†’ `0` for empty routes.
3. **Fix Flake8 issues** â€“ whitespace after commas (E231), two blank lines between functions (E302), lines wrapped to 79 characters (E501).

A baseline commit before these adds the original file and the "before" reports.

## Key issues fixed

| Issue | Severity | Fix |
|-------|----------|-----|
| Shell command injection via `shell=True` (B602) | High | Removed the shell call; message printed directly |
| SQL injection through f-string query (B608) | Medium | `?` placeholders with a values tuple |
| Bare `except` (W0702 / E722) | Medium | Catch `sqlite3.Error` only |
| File opened without `with` / encoding (R1732, W1514) | Medium | Context manager with `encoding="utf-8"` |
| Unused argument `driver` (W0613) | Medium | Parameter removed, callers updated |
| `assert` for runtime check (B101) | Low | `raise ValueError` on mismatch |

The full table of 14 issues is in [`issues.md`](issues.md).

## Behaviour check

The program still does its job. Before and after, `python school_transport.py` prints:

```
dispatching bus R1
['Zoya']
```

and writes `route_r1.txt` containing `Tara` and `Kabir`.

## Reproduce

```bash
python -m venv venv && source venv/bin/activate
pip install pylint bandit flake8
pylint school_transport.py > pylint_report.txt
bandit -r school_transport.py > bandit_report.txt
flake8 school_transport.py > flake8_report.txt
```
