
🚀 Deployment Guide for Vagus-Decipher AI (BIO-MED-02)

Package Deployment (PyPI)

Prerequisites

```bash
pip install build twine
```

Build Package

```bash
python -m build
```

Upload to PyPI (Production)

```bash
twine upload dist/*
```

---

Docker Deployment

Build Image

```bash
docker build -t vagus-decipher:latest .
```

Run Container

```bash
docker run -it --rm vagus-decipher:latest --interface implanted_cuff --steps 1000
```

---

CI/CD Pipeline (GitLab CI)

The .gitlab-ci.yml includes:

1. Test - Run unit tests on Python 3.11-3.12
2. Build - Create PyPI package
3. Deploy - Auto-deploy to PyPI on tags
4. Mirror - Push to GitHub, Bitbucket, Codeberg

Trigger Deployment

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

Netlify Deployment (Documentation)

```bash
cd Netlify/
netlify deploy --prod
```

Configuration

· Site name: vagus-decipher.netlify.app
· Publish directory: Netlify/

---

Repository Mirrors

```bash
git push github main
git push gitlab main
git push bitbucket main
git push codeberg main
```

---

Verification

```bash
pip install vagus-decipher
curl https://doi.org/10.5281/zenodo.20347323
curl https://vagus-decipher.netlify.app
```

---

FPGA Deployment (TensorRT)

```bash
# Export to TensorRT INT8
python -m vagus_decipher.export_tensorrt --precision int8 --target orin

# Run on NVIDIA Jetson Orin
./build/vagus_decipher_trt --interface implanted_cuff --latency-test
```

---

For production deployments, ensure all tests pass and documentation is up to date.
