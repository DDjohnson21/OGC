# OGC Smart Contracts

Smart contracts for the OGC (Out The Groupchat) project.

## Quick Start

```bash
# Install dependencies
make install

# Build contracts
make build

# Run tests
make test

# Run demo
make demo
```

## CI/CD

This project uses GitHub Actions for continuous integration:
- ✅ Builds contracts on every push
- ✅ Runs test suite
- ✅ Validates demo scenarios
- ✅ Uses pinned dependencies for reproducibility

## Dependencies

All dependencies are pinned in `pyproject.toml` for reproducible builds:
- `beaker-pyteal==1.1.1`
- `pyteal==0.24.1` 
- `py-algorand-sdk==2.10.0`
- `algokit-utils==2.4.0`