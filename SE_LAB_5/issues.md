# Lab 5 – Issue Table (`school_transport.py`)

Line numbers refer to the original file. Sorted by severity (high and medium first).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B602 | Security | High | 24 | `subprocess.run("echo dispatching bus " + route, shell=True)` passes user-controlled `route` to a shell, so a value like `R1; del *` would run arbitrary commands. | Removed the shell call; the alert is now printed with `print()`. |
| 2 | SQL injection | Bandit B608 | Security | Medium | 9 | `enrollRider` builds the INSERT with an f-string, so a name like `O'Brien` breaks it and crafted input can inject SQL. | Use a parameterised query with `?` placeholders and a tuple of values. |
| 3 | Bare `except` | Pylint W0702 / Flake8 E722 | Bug | Medium | 30 | `except:` swallows every exception, including `KeyboardInterrupt` and programming errors. | Catch only `sqlite3.Error`. |
| 4 | File not closed safely, no encoding | Pylint R1732, W1514 | Bug | Medium | 18 | `open()` without `with` leaks the file handle if a write fails; no encoding means output depends on the OS locale. | `with open(path, "w", encoding="utf-8") as out:` |
| 5 | Unused argument | Pylint W0613 | Code smell | Medium | 13 | `routeRoster(route, driver)` never uses `driver`; callers pass dummy values. | Removed the parameter and updated the callers. |
| 6 | `assert` used for runtime check | Bandit B101 | Security / Bug | Low | 38 | `assert` is stripped under `python -O`, so the fee check silently disappears. | Replaced with `if ... != 3600: raise ValueError(...)`. |
| 7 | `subprocess` import | Bandit B404 | Security | Low | 1 | Importing `subprocess` is flagged as a potential command-execution risk. | Import removed (no longer needed after fix 1). |
| 8 | Non-snake_case function names | Pylint C0103 | Style | Low | 8, 13, 17, 23, 27 | `enrollRider`, `routeRoster`, … violate PEP 8 naming. | Renamed to `enroll_rider`, `route_roster`, `export_roster`, `dispatch_alert`, `fee_collected`. |
| 9 | Missing docstrings | Pylint C0114, C0116 | Documentation | Low | 1, 8, 13, 17, 23, 27, 34 | No module or function docstrings. | Added a module docstring and one per function. |
| 10 | Lines too long | Pylint C0301 / Flake8 E501 | Style | Low | 5, 9, 14, 29 | Lines up to 116 characters (Pylint limit 100, Flake8 limit 79). | Wrapped lines using implicit string concatenation and argument continuation. |
| 11 | Missing whitespace after comma | Flake8 E231 | Style | Low | 8 | `def enrollRider(student,route,stop,fee)` | Added spaces after commas. |
| 12 | Too few blank lines | Flake8 E302 | Style | Low | 23 | Only 1 blank line before `def dispatchAlert`. | Two blank lines between top-level definitions. |
| 13 | `None` returned for empty route (found while reviewing) | Manual review | Bug | Low | 29 | `SUM(fee)` over zero rows returns `NULL`, so `feeCollected("R9")` returned `None` instead of `0`. | `return total or 0`. |
| 14 | Code runs on import | Manual review | Design | Low | 44 | `main()` was called at module level, so importing the module ran the demo. | Wrapped in `if __name__ == "__main__":`. |
