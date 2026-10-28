# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.7] 2026-10-29 00:44:33

### Fixed

- `is_pytest_active()` and `is_testenv_active()` called without an `arg_string` return `True`
  inside a pytest-xdist worker. A worker runs as `python -c`, so its `sys.argv` names neither
  pytest nor a test file and both returned `False` there; they now also check the
  `PYTEST_XDIST_WORKER` variable xdist sets in every worker. A call given an `arg_string` is still
  judged on that string alone.

### Tests

- The suite runs in parallel: `pytest-xdist` joins the dev extra and the `workers = 1` setting that
  kept `make test` serial is gone.

## [3.0.6] 2026-10-15 16:35:25

### Fixed

- The source distribution ships only the package, its tests, its docs, `README.md`, `LICENSE`,
  `CHANGELOG.md` and `pyproject.toml` (an include list). Earlier sdists also carried every other
  root file and, in a local build, anything hidden only through `.git/info/exclude` or a nested
  `.gitignore`. `tests/test_packaging.py` builds the sdist and wheel and checks both; `hatchling`
  joins the dev extra for it.

### Changed

- Ruff selects `C90` (mccabe), so a function over cyclomatic complexity 10, the house hard limit,
  now fails `make test`; before, nothing enforced it.

### Tests

- The `os_windows`, `os_macos`, `os_linux` and `os_posix` markers now skip a test off its platform
  (`pytest_runtest_setup` in `tests/conftest.py`); registered in `pyproject.toml` alone they skipped
  nothing, so a test trusting its marker ran everywhere. `tests/test_platform_markers.py` pins it.

## [3.0.5] 2026-10-15 14:11:33

### Added
- Python 3.15 is a supported version: declared in the classifiers, so CI and `make test-all` run it.
- `uv.lock` is committed, and `[tool.uv] exclude-newer` sets a cooldown that keeps releases younger
  than it out of the lock. CI installs exactly the locked tree on push and pull request; the nightly
  scheduled run still resolves afresh to catch upstream breakage early.

### Changed
- The install section explains why installing with uv protects against supply-chain attacks and why
  a plain `pip install` from PyPI does not.
- `rtoml` floor raised to 0.14.0, the first release with Python 3.15 wheels.

## [3.0.4] 2026-08-01 00:14:59
### Fixed
- **Console output no longer crashes on a legacy codepage.** A Windows console at codepage 1252
  hands Python an `errors="strict"` stream, so writing a non-ASCII character such as a check mark
  raised `UnicodeEncodeError: 'charmap' codec can't encode character` and the command exited
  non-zero *after* its work had already succeeded. Click does not protect against this, and Rich
  raises the same way through its own writer. The new `safe_console` module degrades at the sink:
  a UTF-8 terminal still receives the character, and only a stream that cannot encode it sees
  `[OK]` / `[X]` / `[!]`. Every `click.echo` call site routes through it, and a test fails if a
  module reaches for `click.echo` or builds an unwrapped `Console(file=sys.stdout)` again.


## [3.0.3] 2026-07-24 16:01:54

### Fixed
- Fixed CI going red under the latest ruff (0.16 widened its default rule set to ~920 rules on a
  repo with no explicit `[tool.ruff.lint].select`): pinned the curated bitranox rule select instead
  of chasing the exploded default set.
- `raise SystemExit(2)` in the CLI's error handlers now uses `from e` so tracebacks show the
  original cause (B904).
- `print_info()` and the `__main__` guard now write via `sys.stdout`/`sys.stderr` instead of `print`,
  fixing a latent bug where the guard printed a `bytes` literal's repr instead of the plain message.

### Changed
- Added the curated `[tool.ruff.lint].select` (matching `bitranox_template_py_cli`) plus
  `pydocstyle` Google convention and a `tests/*.py` per-file-ignore list, replacing the previous
  no-`select` config that inherited ruff's entire default rule set.
- Made the Click CLI callback parameters keyword-only (`*,`) so ruff's `PLR0917` no longer fires;
  Click already invokes command callbacks by keyword, so this is not a call-site change.
- Simplified boolean-returning `if/return True/False` branches in `lib_detect_testenv.py` to direct
  `return <condition>` expressions (SIM103).
- Moved two deferred, no-reason `import sys`/`from rich.style import Style` statements in `cli.py`
  to the module top (PLC0415).
- Replaced `Optional[X]` with `X | None` throughout `cli.py` (UP045).

## [3.0.2] 2026-06-14

### Changed
- Added a `typed_click.py` facade wrapping rich-click's `option` / `version_option` decorators behind explicit, fully-known signatures, keeping the CLI strict-clean under pyright (`reportUnknownMemberType`). The repo-wide `reportUnknownMemberType` suppression is retained, but only for the `tomli` backport (untyped on Python 3.10); the rich-click decorators no longer rely on it.
- Migrated build automation from the in-repo `scripts/` package to the external `bmk` tooling (`uvx bmk`); removed the obsolete `scripts/` directory and `[tool.scripts.test]` config; added `[tool.bashate]` settings and the bmk CI workflows.

### Removed
- Dropped Python 3.9 support (`requires-python>=3.10`): the bmk build/dev toolchain requires Python 3.10+.

## [3.0.1] - 2025-12-15

### Changed

- Replaced `tomllib`/`tomli` with `rtoml` for TOML parsing in scripts
- Updated GitHub Actions dependencies:
  - `actions/cache` v4 → v5
  - `actions/upload-artifact` v5 → v6
- Added `PYTHONIOENCODING: "utf-8"` environment variable to CI workflow for consistent encoding

## [3.0.0] - 2025-11-04

### Added

**Core Library Features:**
- `add_path_to_syspath()` function to add paths to sys.path with duplicate prevention
- Full support for PathLike objects and string paths
- Automatic resolution of relative paths to absolute paths
- File path handling (adds parent directory when given a file)

**CLI Detection Commands:**
- `check` - Check if any test environment is active (pytest, doctest, setup.py test)
- `pytest` - Check if pytest is active
- `doctest` - Check if doctest is active
- `setup` - Check if setup.py is active
- `--quiet` flag for all detection commands (exit code only, no output)
- `--arg-string` option to test custom argument strings
- `--test-only` flag for setup command (check only "setup.py test")

**CLI Utility Commands:**
- `hello` - Demo command to print greeting message
- `fail` - Demo command to trigger intentional failure for testing error handling
- `info` - Display package metadata and version information

**3-Level Exit Code System:**
- Exit code **0** = Test environment detected (success)
- Exit code **1** = No test environment detected (normal negative result)
- Exit code **2** = Error occurred (command failed with exception)
- Follows Unix conventions for intuitive shell scripting
- All detection commands implement consistent exit code behavior

**Comprehensive Test Suite:**
- 68 tests total (100% passing rate)
- 28 tests for core library functions (test_lib_detect_testenv.py)
  - Tests for all detection functions
  - Tests for add_path_to_syspath with edge cases
  - Tests for PathLike support and duplicate prevention
- 23 tests for CLI commands (test_cli.py)
  - Tests for all detection commands
  - Tests for exit codes
  - Tests for quiet mode and flags
- Full coverage of test environment detection scenarios

**Documentation:**
- Comprehensive README.md with CLI and Python API usage
- Exit code documentation with shell scripting examples
- Function reference with parameters, returns, and examples
- Common usage patterns section
- INSTALL.md updated for optional dependencies

### Changed

**BREAKING CHANGES:**
- Renamed internal module `detect_testenv.py` to `lib_detect_testenv.py`
- Minimal dependencies - Only `rich-click>=1.9.4` required for CLI functionality
  - `dependencies = ["rich-click>=1.9.4"]` - Required for CLI entry point
  - Core detection library functions have no external dependencies (pure stdlib)
  - Users can import detection functions (`is_pytest_active()`, etc.) without using rich-click
  - CLI commands require rich-click for beautiful terminal output

**Configuration:**
- Keywords updated from `["logging", "rich", "cli", "terminal", "ansi"]` to `["testing", "pytest", "doctest", "unittest", "test-detection", "test-environment"]` for accurate PyPI discoverability
- Import linter configuration updated to check correct architecture (CLI → lib_detect_testenv → behaviors)
- pyproject.toml restructured with optional dependency groups

**Documentation:**
- Updated README.md from RST format to Markdown with:
  - Complete function reference documentation
  - CLI usage examples with exit code explanations
  - Shell scripting patterns and best practices
  - Common usage patterns section
- Default CLI behavior now runs `check` command when invoked without arguments
- All CLI commands documented with examples

### Fixed
- CLI now uses actual library detection functions instead of template boilerplate
- Import paths updated throughout codebase to reflect renamed module
- Documentation accurately reflects actual functionality
- All 68 tests passing with proper coverage of core functionality
- Exit code handling consistent across all detection commands
- Error handling improved with try/except blocks returning exit code 2

### Documentation Improvements
- Added comprehensive 3-level exit code system documentation
- Added shell scripting examples for all detection commands
- Documented hello/fail demo commands
- Added comprehensive Python API reference with all function signatures
- Exit code handling examples for different shell scripting scenarios
- Added case statement examples for handling all three exit codes

## [1.0.0] - 2025-11-04
- Bootstrap `lib_detect_testenv`
