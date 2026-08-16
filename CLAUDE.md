# Claude Code Guidelines for lib_detect_testenv

## Project Structure

```
lib_detect_testenv/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD workflows
├── .devcontainer/              # Dev container configuration
├── docs/                       # Project documentation
│   └── systemdesign/           # System design documents
├── notebooks/                  # Jupyter notebooks for experiments
├── scripts/                    # Build and automation scripts
│   ├── build.py               # Build wheel/sdist
│   ├── bump.py                # Version bump (generic)
│   ├── bump_major.py          # Bump major version
│   ├── bump_minor.py          # Bump minor version
│   ├── bump_patch.py          # Bump patch version
│   ├── bump_version.py        # Version bump utilities
│   ├── clean.py               # Clean build artifacts
│   ├── cli.py                 # CLI for scripts
│   ├── dependencies.py        # Dependency management
│   ├── dev.py                 # Development install
│   ├── help.py                # Show help
│   ├── install.py             # Install package
│   ├── menu.py                # Interactive TUI menu
│   ├── push.py                # Git push
│   ├── release.py             # Create releases
│   ├── run_cli.py             # Run CLI
│   ├── target_metadata.py     # Metadata generation
│   ├── test.py                # Run tests with coverage
│   ├── toml_config.py         # TOML configuration utilities
│   ├── version_current.py     # Print current version
│   └── _utils.py              # Shared utilities
├── src/
│   └── lib_detect_testenv/    # Main Python package
│       ├── __init__.py        # Package initialization & public API
│       ├── __init__conf__.py  # Configuration constants
│       ├── __main__.py        # CLI entry point
│       ├── behaviors.py       # Domain behaviors (greeting, failure hooks)
│       ├── cli.py             # CLI implementation
│       ├── lib_detect_testenv.py  # Core detection functions
│       └── py.typed           # PEP 561 marker
├── tests/                     # Test suite
│   ├── conftest.py            # Pytest fixtures
│   ├── test_behaviors.py      # Behavior tests
│   ├── test_cli.py            # CLI tests
│   ├── test_lib_detect_testenv.py  # Core library tests
│   ├── test_metadata.py       # Metadata tests
│   ├── test_module_entry.py   # Module entry tests
│   └── test_scripts.py        # Script tests
├── .env.example               # Example environment variables
├── CLAUDE.md                  # Claude Code guidelines (this file)
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── DEVELOPMENT.md             # Development setup guide
├── INSTALL.md                 # Installation instructions
├── LICENSE                    # MIT License
├── Makefile                   # Make targets for common tasks
├── pyproject.toml             # Project metadata & dependencies
├── codecov.yml                # Codecov configuration
└── README.md                  # Project overview
```

## Versioning & Releases

- **Single Source of Truth**: Package version is in `pyproject.toml` (`[project].version`)
- **Version Bumps**: update `pyproject.toml`, `CHANGELOG.md` and update the constants in `src/lib_detect_testenv/__init__conf__.py` according to `pyproject.toml`
    - Automation rewrites `src/lib_detect_testenv/__init__conf__.py` from `pyproject.toml`, so runtime code imports generated constants instead of querying `importlib.metadata`.
    - After updating project metadata (version, summary, URLs, authors) run `make test` (or `python -m scripts.test`) to regenerate the metadata module before committing.
- **Release Tags**: Format is `vX.Y.Z` (push tags for CI to build and publish)

## Make targets specific to this repo

- `make run` - Run module entry (`python -m ... --help`)

Everything else is the generated bmk list: run `make help`.

## Architecture Overview

This library provides test environment detection with a simple layered structure:

- **lib_detect_testenv.py**: Core detection functions (`is_testenv_active`, `is_pytest_active`, `is_doctest_active`, etc.)
- **behaviors.py**: Domain behaviors (greeting, failure hooks for CLI testing)
- **cli.py**: CLI interface using rich-click

Import rules (enforced by import-linter):
- `cli` depends on `lib_detect_testenv` and `behaviors`
- Core detection functions have no internal dependencies

Apply principles use skill `bitranox:coding-python-clean-architecture` when designing and implementing features.

## Commit & Push Policy

### Pre-Push Requirements
- **Always run `make test` before pushing** to avoid lint/test breakage
- Ensure all tests pass and code is properly formatted

### Post-Push Monitoring
- Monitor GitHub Actions for errors after pushing
- Attempt to correct any CI/CD errors that appear

