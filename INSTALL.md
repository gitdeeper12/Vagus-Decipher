
📦 Installation Guide for Vagus-Decipher AI (BIO-MED-02)

Quick Install (PyPI)

```bash
pip install vagus-decipher
```

Install from Source

```bash
git clone https://github.com/gitdeeper12/Vagus-Decipher.git
cd Vagus-Decipher
pip install -e .
```

Verify Installation

```python
import vagus_decipher
print(vagus_decipher.__version__)  # 1.0.0
print(vagus_decipher.__doi__)      # 10.5281/zenodo.20347323
```

```bash
python -c "from vagus_decipher import VagusDecipherEngine; print('Vagus-Decipher ready')"
```

---

Requirements

Package Version Required
Python ≥ 3.11
torch ≥ 2.4.0
numpy ≥ 2.0.0
scipy ≥ 1.14.0
pywavelets ≥ 1.5.0
filterpy ≥ 1.4.5

---

Platform Support

Platform Support
Linux ✅ Fully tested
macOS ✅ Compatible
Windows ✅ Compatible
Termux (Android) ✅ Compatible
NVIDIA Jetson Orin ✅ TensorRT supported

---

Docker Installation

```bash
docker pull gitdeeper12/vagus-decipher:latest
docker run --rm vagus-decipher --help
```

---

Uninstall

```bash
pip uninstall vagus-decipher
rm -rf Vagus-Decipher
```

---

For issues, open a ticket on GitHub/GitLab.
