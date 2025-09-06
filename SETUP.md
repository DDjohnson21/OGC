# OGC Development Setup

## 🚀 Fresh AlgoKit Setup

If you just installed AlgoKit and want to start:

### 1. Install AlgoKit
```bash
# Install AlgoKit
pipx install algokit

# Verify installation
algokit --version
algokit doctor  # Check system health
```

### 2. Start LocalNet
```bash
# Start Algorand LocalNet
algokit localnet start

# Check status
algokit localnet status
```

### 3. Navigate to Project
```bash
cd ~/OGC/ogc-contracts/projects/ogc-contracts
```

### 4. Activate Environment
```bash
# Activate Poetry virtualenv
source "$(poetry env info --path)/bin/activate"

# Verify Python version
python --version  # Should be 3.13.x
```

### 5. Install Dependencies
```bash
# Install with Poetry
poetry install

# Or manually with pip
pip install beaker-pyteal pyteal py-algorand-sdk algokit-utils
```

### 6. Build & Test
```bash
# Build contracts
python working_vault.py

# Run tests
python test_vault.py

# Run demo
python ogc_demo.py
```

### 7. Stop When Done
```bash
# Stop LocalNet
algokit localnet stop
```

## 🔄 Quick Reset Script

If you need to reset your environment:

```bash
# One-liner to get back into dev mode
cd ~/OGC/ogc-contracts/projects/ogc-contracts && source "$(poetry env info --path)/bin/activate" && python --version
```

Or use the Makefile:
```bash
make dev  # Activates environment and drops into shell
```

## 🛠️ Development Commands

```bash
make install  # Install dependencies
make build    # Build contracts
make test     # Run tests
make demo     # Run demo
make ci       # Full CI pipeline
```

## 🔍 Troubleshooting

**LocalNet not starting?**
```bash
algokit localnet reset  # Reset LocalNet
algokit doctor          # Check system health
```

**Python version issues?**
```bash
poetry env info         # Check Poetry environment
poetry shell           # Alternative to source activation
```

**Dependencies not found?**
```bash
poetry install --no-cache  # Reinstall dependencies
```

## 📁 Project Structure

```
OGC/
├── SETUP.md                    # This file
├── .github/workflows/ci.yml    # CI configuration
└── ogc-contracts/projects/ogc-contracts/
    ├── pyproject.toml          # Dependencies
    ├── Makefile               # Build commands
    ├── working_vault.py       # Main contract
    ├── test_vault.py         # Tests
    └── ogc_demo.py           # Demo
```