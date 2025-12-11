# Kurulu Paketten Wheel Oluşturma Rehberi

## Senaryo
Sisteminde kurulu olan bir Python paketi artık internetten indirilemiyor veya eski bir sürüm. Bu paketi wheel haline getirip başka sistemlere taşımak istiyorsun.

---

## Yöntem 1: pip-wheel Komutu (En Kolay)

### Kurulu Paketten Direkt Wheel
```bash
# Paketi bul ve wheel oluştur
pip wheel <paket_adi> --no-deps --wheel-dir=./my-wheels

# Örnek
pip wheel numpy==1.21.0 --no-deps --wheel-dir=./my-wheels
```

**Not:** `--no-deps` bayrağı bağımlılıkları dahil etmez, sadece o paketi wheel yapar.

---

## Yöntem 2: Wheel Paketi ile (Önerilen)

### Adım 1: Wheel Paketini Kur
```bash
pip install wheel
```

### Adım 2: Site-Packages'dan Wheel Oluştur
```bash
# Paketin kurulu olduğu yeri bul
python -c "import torch; print(torch.__path__[0])"
# Çıktı: /home/user/.local/lib/python3.8/site-packages/torch

# O dizinden wheel oluştur
cd /home/user/.local/lib/python3.8/site-packages/
python -m wheel pack torch
```

Bu yöntem bazen çalışmayabilir, o zaman Yöntem 3'ü kullan.

---

## Yöntem 3: Pip Show + Manuel Paketleme (En Güvenilir)

### Adım 1: Paket Bilgilerini Öğren
```bash
pip show torch

# Çıktı:
# Name: torch
# Version: 2.0.0
# Location: /home/user/.local/lib/python3.8/site-packages
```

### Adım 2: Site-Packages Dizinini Bul
```bash
python -c "import site; print(site.getsitepackages())"
# veya
python -c "import torch; print(torch.__file__)"
```

### Adım 3: Paketi Yeniden Kur (Wheel Oluşturarak)
```bash
# Cache'i temizle
pip cache purge

# Paketi wheel olarak "indir" (aslında yeniden kur)
pip wheel torch==2.0.0 --no-deps --wheel-dir=./wheels

# Eğer cache'de varsa direkt wheel oluşur
```

---

## Yöntem 4: Setup.py Varsa (Source Distribution)

### Paket Kaynak Kodunu Bul
```bash
# Kurulu paketin konumunu öğren
pip show -f torch | grep Location
cd /path/to/torch

# setup.py varsa
python setup.py bdist_wheel

# dist/ klasöründe wheel oluşur
ls dist/
# torch-2.0.0-cp38-cp38-linux_aarch64.whl
```

---

## Yöntem 5: Pip Cache'den Wheel Çıkarma

### Cache'i Kontrol Et
```bash
# Pip cache'ini listele
pip cache list torch

# Cache dizinini bul
pip cache info
# Location: /home/user/.cache/pip
```

### Cache'den Wheel Kopyala
```bash
cd ~/.cache/pip/wheels/
find . -name "*torch*"

# Bulduğun wheel'i kopyala
cp ./xx/xx/torch-2.0.0-cp38-linux_aarch64.whl ~/my-wheels/
```

---

## Yöntem 6: Manuel Arşivleme (Son Çare)

### Adım 1: Paket Dizinini Bul ve Kopyala
```bash
# Paketin yerini öğren
python -c "import torch; print(torch.__path__[0])"

# Paketi kopyala
cp -r /path/to/site-packages/torch ~/backup-packages/torch
cp -r /path/to/site-packages/torch-2.0.0.dist-info ~/backup-packages/torch-2.0.0.dist-info
```

### Adım 2: Geçici Setup Dosyası Oluştur
```bash
cd ~/backup-packages/

# setup.py oluştur
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='torch',
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
)
EOF
```

### Adım 3: Wheel Oluştur
```bash
python setup.py bdist_wheel
ls dist/
# torch-2.0.0-py3-none-any.whl
```

---

## Yöntem 7: Docker Container'dan Çıkarma

### Eski Sürüm Docker Image'ı Varsa
```bash
# Container çalıştır
docker run -it --name old_env python:3.8

# Container içinde paketi kur
pip install torch==1.8.0

# Wheel'i oluştur
pip wheel torch==1.8.0 --no-deps --wheel-dir=/tmp/wheels

# Host'a kopyala
docker cp old_env:/tmp/wheels/torch-1.8.0.whl ./
```

---

## Özel Durum: C Extension'lı Paketler

### Numpy, PyTorch, TensorFlow gibi
```bash
# Bu paketler platform spesifik!
# Wheel dosyası isminde platform bilgisi olmalı

# Jetson'da kurulu numpy'den wheel:
pip wheel numpy --no-deps --wheel-dir=./wheels

# Oluşan wheel:
# numpy-1.21.0-cp38-cp38-linux_aarch64.whl
#                          ^^^^^^^^^^^^^^
#                          Platform bilgisi
```

**Önemli:** Bu wheel sadece aynı platformda (ARM64) çalışır!

---

## Pratik Örnek: Tüm Sistemi Yedekleme

### Tüm Kurulu Paketleri Wheel Yap
```bash
# Kurulu paketleri listele
pip list --format=freeze > requirements.txt

# Tüm paketleri wheel'e çevir
mkdir all-wheels
pip wheel -r requirements.txt --wheel-dir=./all-wheels

# Başka sisteme taşı
tar -czf jetson-wheels-backup.tar.gz all-wheels/
```

---

## Hızlı Komutlar Özeti

```bash
# Yöntem 1: Direkt wheel oluştur
pip wheel <paket> --no-deps --wheel-dir=./wheels

# Yöntem 2: Cache'den bul
pip cache list <paket>

# Yöntem 3: Yeniden kur ve wheel al
pip install <paket> --download ./wheels --no-deps

# Yöntem 4: Manuel setup.py
python setup.py bdist_wheel
```

---

## Sorun Giderme

### "No matching distribution found"
```bash
# Paketi belirli versiyonla bul
pip download torch==2.0.0 --no-deps --dest ./wheels

# Eğer bulamazsa, cache'i kontrol et
pip cache list | grep torch
```

### "Binary incompatible"
```bash
# Platform bilgisini kontrol et
file /path/to/package.so

# ARM için wheel oluştururken:
python setup.py bdist_wheel --plat-name=linux_aarch64
```

### Setup.py Yok
```bash
# Paket dizininde pyproject.toml varsa:
pip install build
python -m build --wheel
```

---

## Sonuç

En güvenilir yöntem sırası:
1. ✅ `pip wheel <paket> --no-deps` (En kolay)
2. ✅ Pip cache'den bulma (Hızlı)
3. ✅ Manuel setup.py ile wheel oluşturma (Kontrollü)
4. ⚠️ Site-packages'ı direkt kopyalama (Son çare)

**Hatırla:** C extension'lı paketler platform spesifiktir! Jetson'da oluşturduğun wheel başka ARM64 cihazlarda çalışır, ama x86 PC'de çalışmaz.