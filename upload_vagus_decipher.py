#!/usr/bin/env python3

"""Vagus-Decipher Upload v1.0.0 - PyPI"""

import requests
import hashlib
import os
import glob

TOKEN = ""

print("="*60)
print("🧬 Vagus-Decipher v1.0.0 Upload - PyPI")
print("="*60)
print("Neural Decoding of Vagus Nerve Electrophysiology")
print("for Real-Time Prediction of Systemic Inflammatory Storms")
print("="*60)

# قراءة README.md
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    print(f"\n📄 README.md: {len(readme)} characters")
except FileNotFoundError:
    print("\n⚠️ README.md not found, using fallback description")
    readme = "Vagus-Decipher AI: Neural Decoding of Vagus Nerve Electrophysiology for Real-Time Prediction of Systemic Inflammatory Storms"

# البحث عن ملفات التوزيع
wheel_files = glob.glob("dist/*.whl")
tar_files = glob.glob("dist/*.tar.gz")

if not wheel_files and not tar_files:
    print("\n❌ No distribution files found. Building package...")
    os.system("python -m build")
    
    wheel_files = glob.glob("dist/*.whl")
    tar_files = glob.glob("dist/*.tar.gz")

print(f"\n📦 Distribution files:")
for f in wheel_files + tar_files:
    print(f"   • {os.path.basename(f)}")

upload_success = False

for filepath in wheel_files + tar_files:
    filename = os.path.basename(filepath)
    print(f"\n📤 Uploading: {filename}")

    # تحديد نوع الملف
    if filename.endswith('.tar.gz'):
        filetype = 'sdist'
        pyversion = 'source'
    else:
        filetype = 'bdist_wheel'
        pyversion = 'py3'

    # حساب الهاشات
    with open(filepath, 'rb') as f:
        content = f.read()
    md5_hash = hashlib.md5(content).hexdigest()
    sha256_hash = hashlib.sha256(content).hexdigest()

    # بيانات الرفع لـ Vagus-Decipher
    data = {
        ':action': 'file_upload',
        'metadata_version': '2.1',
        'name': 'vagus-decipher',
        'version': '1.0.0',
        'filetype': filetype,
        'pyversion': pyversion,
        'md5_digest': md5_hash,
        'sha256_digest': sha256_hash,
        'description': readme,
        'description_content_type': 'text/markdown',
        'author': 'Samir Baladi',
        'author_email': 'gitdeeper@gmail.com',
        'license': 'MIT',
        'summary': 'Vagus-Decipher AI: Neural Decoding of Vagus Nerve Electrophysiology for Real-Time Prediction of Systemic Inflammatory Storms',
        'home_page': 'https://vagus-decipher.netlify.app',
        'requires_python': '>=3.11',
        'keywords': 'vagus-nerve, electroneurogram, neural-decoding, inflammatory-storm, septic-shock, cytokine-release-syndrome, wavelet-transform, state-space-model, physics-informed-neural-network, neuroimmunology, biomedical-ai'
    }

    # رفع الملف
    try:
        with open(filepath, 'rb') as f:
            response = requests.post(
                'https://upload.pypi.org/legacy/',
                files={'content': (filename, f, 'application/octet-stream')},
                data=data,
                auth=('__token__', TOKEN),
                timeout=90,
                headers={'User-Agent': 'Vagus-Decipher-Uploader/1.0'}
            )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print("   ✅✅✅ SUCCESS!")
            upload_success = True
        else:
            print(f"   ❌ Error: {response.text[:300]}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

print("\n" + "="*60)
if upload_success:
    print("✅ Vagus-Decipher v1.0.0 uploaded successfully!")
    print("🔗 https://pypi.org/project/vagus-decipher/1.0.0/")
else:
    print("⚠️ Upload completed with some issues.")
    print("🔗 https://pypi.org/project/vagus-decipher/")
print("="*60)

print("\n📦 Install Vagus-Decipher:")
print("   pip install vagus-decipher")
print("")
print("📖 Documentation:")
print("   https://vagus-decipher.netlify.app")
