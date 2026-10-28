# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues (E231 missing spaces, E302 blank lines) and the Pylint docstring/naming warnings: they are mechanical and the tool tells you exactly what to change. The hardest were the security findings. The SQL injection (B608) needed the query rewritten with `?` placeholders rather than just escaping quotes, and the `shell=True` call (B602) needed a decision about what the function should actually do; since it only echoed a message, the safest fix was to drop `subprocess` entirely and print. Renaming functions was also slightly tricky because every caller had to be updated consistently, and removing the unused `driver` argument changed the function signature.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit B101 (`assert` used) is close to a false positive in a small demo script, because the assert was only a sanity check in `main()` and not a security control. It is still worth fixing because `python -O` removes asserts, so I replaced it with an explicit `raise ValueError`. B404 (importing `subprocess`) is informational: importing the module is not unsafe by itself; the real problem was the `shell=True` call. Pylint's line-length limit (100) and Flake8's (79) also disagree, so a line can pass one tool and fail the other.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- Run Flake8 and Pylint in the editor while writing code, so issues are fixed right away.
- Add a `pre-commit` hook that runs Flake8, Pylint and Bandit on staged files, so badly formatted or insecure code is never committed.
- Run all three in CI (e.g. a GitHub Actions workflow) on every pull request, fail the build on any Bandit High/Medium finding or a Pylint score below 9.5, and upload the reports as artifacts.
- Keep shared configuration (`.pylintrc`, `setup.cfg`/`.flake8`, line length) in the repo so everyone gets the same results, and require a justification comment for any `# nosec` or `# pylint: disable`.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** Bandit went from 4 issues (1 High, 1 Medium, 2 Low) to 0; names like `O'Brien` no longer break inserts, and route names can no longer run shell commands.
- **Quality:** Pylint went from 4.00/10 to 10.00/10, and Flake8 from 9 violations to 0.
- **Robustness:** the roster file is always closed (with UTF-8 encoding), database errors are caught specifically instead of everything being swallowed, `fee_collected` now returns `0` instead of `None` for an empty route, and the fee check survives `python -O`.
- **Readability:** snake_case names, docstrings and short lines make the module easier to read, and the `__main__` guard means it can be imported without running the demo.

The program output is unchanged: `dispatching bus R1` followed by `['Zoya']`, and `route_r1.txt` contains `Tara` and `Kabir`.
