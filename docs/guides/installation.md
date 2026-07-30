# Installation & Setup Guide

## Prerequisites

- **Python**: 3.11 or higher.
- **Git**: Installed and available on system PATH.

---

## Installation Steps

### 1. Install via pip
```bash
pip install profileforge
```

### 2. Install from Source for Development
```bash
git clone https://github.com/anujmundu/ProfileForge.git
cd ProfileForge
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

---

## Verifying Installation

Run the quality gate test suite:
```bash
pytest
```
Expected output: `100+ passed`
