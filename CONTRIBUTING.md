# Contributing to Vagus-Decipher AI (BIO-MED-02)

Thank you for your interest in contributing to **Vagus-Decipher AI**!

## How to Contribute

### 1. Report Bugs
- Use GitHub/GitLab Issues
- Include: Python version, hardware interface, steps to reproduce
- Label: `bug`

### 2. Suggest Features
- Open an issue with label `enhancement`
- Describe the use case and expected behavior
- New cytokine targets or clinical thresholds are welcome

### 3. Submit Code Changes

#### Prerequisites
```bash
pip install -e .[dev]
pre-commit install
```

Development Workflow

```bash
git clone https://github.com/gitdeeper12/Vagus-Decipher
cd Vagus-Decipher
git checkout -b feature/your-feature-name
pytest tests/ -v
git commit -m "feat: add new cytokine target"
git push origin feature/your-feature-name
```

1. Update Documentation

· Edit README.md, docs/, or docstrings
· Ensure clinical thresholds are documented

Code Style

· Python: PEP 8 (use black)
· Type hints: Required for all public functions
· Docstrings: Google style

Testing Requirements

· All tests must pass: pytest tests/ -v
· Coverage should not decrease: pytest --cov=vagus_decipher
· New features require tests
· AWIE, NISSD, ISI components must maintain accuracy

Commit Convention

Type Description
feat New feature
fix Bug fix
docs Documentation
test Testing
refactor Code refactor
perf Performance improvement

Questions?

Open an issue or email: gitdeeper@gmail.com

---

Thank you for contributing to neural decoding of inflammatory storms! 🧠
