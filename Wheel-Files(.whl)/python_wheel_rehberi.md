# Python Paketlerini Wheel Dosyasına Çevirme Rehberi

## Wheel Nedir?
Wheel (`.whl`), Python paketlerinin önceden derlenmiş, kuruluma hazır dağıtım formatıdır.

---

## Yöntem 1: Kurulu Paketten Wheel Oluşturma

### Pip Wheel Komutu
```bash
# Belirli bir paketi wheel'e çevir
pip wheel torch==2.0.0

# Tüm bağımlılıklarla birlikte
pip wheel torch==2.0.0 --wheel-dir=./wheels

# Platform spesifik (Jetson için)
pip wheel torch==2.0.0 --platform linux_aarch64
```

### Kurulu Paketi Yeniden Paketleme
```bash
# Kurulu paketten wheel oluştur
pip wheel numpy --no-deps --wheel-dir=./wheels
```

---

## Yöntem 2: Source'dan Wheel Oluşturma

### Setup.py ile
```bash
# Proje dizininde
cd my-package/

# Wheel oluştur
python setup.py bdist_wheel

# Wheel dosyası dist/ klasöründe oluşur
ls dist/
# my_package-1.0.0-py3-none-any.whl
```

### Poetry ile
```bash
cd my-package/
poetry build

# Wheel dosyası dist/ klasöründe
```

### Build Tool ile (Modern Yöntem)
```bash
pip install build

# Proje dizininde
python -m build --wheel

# dist/ klasöründe wheel oluşur
```

---

## Yöntem 3: Git Repository'den Wheel

```bash
# GitHub'dan direkt wheel oluştur
pip wheel git+https://github.com/user/repo.git

# Belirli branch'ten
pip wheel git+https://github.com/user/repo.git@develop
```

---

## Yöntem 4: Requirements.txt'ten Toplu Wheel

```bash
# requirements.txt'teki tüm paketleri wheel'e çevir
pip wheel -r requirements.txt --wheel-dir=./wheels

# Sadece platform için
pip wheel -r requirements.txt --wheel-dir=./wheels --platform linux_aarch64
```

---

## Jetson için Özel: CUDA Destekli Wheel

### PyTorch için
```bash
cd pytorch/

# ARM + CUDA ile derle
export USE_CUDA=1
export USE_CUDNN=1
export TORCH_CUDA_ARCH_LIST="8.7"  # Orin NX için

python setup.py bdist_wheel
```

### TensorFlow için
```bash
# NVIDIA'dan hazır wheel indir
wget https://developer.download.nvidia.com/compute/redist/jp/v511/tensorflow/tensorflow-2.13.0+nv23.08-cp38-cp38-linux_aarch64.whl
```

---

## Wheel Dosyasını İnceleme

```bash
# İçeriğini görüntüle
unzip -l package.whl

# Metadata'yı oku
wheel unpack package.whl
cat package-1.0.0/package-1.0.0.dist-info/METADATA
```

---

## Pratik Kullanım Senaryoları

### 1. Offline Kurulum için Paket Toplama
```bash
# Tüm bağımlılıklarla
mkdir jetson-wheels
pip download torch torchvision -d jetson-wheels --platform linux_aarch64

# Kurulum
pip install --no-index --find-links=./jetson-wheels torch torchvision
```

### 2. Custom Paket Dağıtımı
```bash
# Kendi paketini wheel yap
cd my-cv-project/
python setup.py bdist_wheel

# Başkalarına gönder
scp dist/my_cv_project-1.0.0-py3-none-any.whl user@jetson:/tmp/
```

### 3. Modifiye Edilmiş Paket
```bash
# Kaynak kodunu düzenle
cd ultralytics/
# ... kod değişiklikleri ...

# Yeni wheel oluştur
python setup.py bdist_wheel

# Kendi wheel'ini kur
pip install dist/ultralytics-8.0.0-py3-none-any.whl --force-reinstall
```

---

## Önemli Notlar

- ✅ **Pure Python** paketler (C kodu yok) → `py3-none-any.whl` (her platformda çalışır)
- ⚠️ **C/C++ Extension** paketler → Platform spesifik wheel gerekir (`linux_aarch64`)
- ⚠️ **CUDA paketleri** → Jetson'da derlenmelidir, x86 wheel'i çalışmaz
- 🔧 Wheel oluşturmak için `wheel` ve `setuptools` paketleri gerekli:
  ```bash
  pip install wheel setuptools build
  ```

---

## Hızlı Referans

| Komut | Açıklama |
|-------|----------|
| `pip wheel <paket>` | Paketi wheel'e çevir |
| `python setup.py bdist_wheel` | Source'dan wheel oluştur |
| `pip download -d ./wheels <paket>` | Wheel'leri indir |
| `pip install --no-index --find-links=./wheels <paket>` | Offline kurulum |