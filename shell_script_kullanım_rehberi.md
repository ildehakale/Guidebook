# Shell Script (.sh) Kullanım Rehberi

## İçindekiler
1. [Temel Kavramlar](#temel-kavramlar)
2. [Shell Script Oluşturma](#shell-script-oluşturma)
3. [Kurulum Script'i Oluşturma](#kurulum-scripti-oluşturma)
4. [Pratik Örnekler](#pratik-örnekler)
5. [İleri Seviye Konular](#ileri-seviye-konular)

---

## Temel Kavramlar

### Shell Script Nedir?

Shell script, Linux/Unix sistemlerinde komutları otomatikleştirmek için kullanılan metin tabanlı dosyalardır. `.sh` uzantısı ile saklanırlar.

### Shebang (#!/bin/bash)

Her shell script'in ilk satırı, hangi yorumlayıcının kullanılacağını belirtir:

```bash
#!/bin/bash          # Bash shell kullan
#!/bin/sh            # POSIX uyumlu shell
#!/usr/bin/env bash  # Sistemdeki bash'i bul ve kullan (tavsiye edilen)
```

---

## Shell Script Oluşturma

### 1. Basit Bir Script

```bash
#!/bin/bash

echo "Merhaba Dünya!"
echo "Bu benim ilk shell scriptim"
```

### 2. Script'i Çalıştırılabilir Yapma

```bash
# İzin ver
chmod +x script.sh

# Çalıştır
./script.sh
```

### 3. Değişkenler

```bash
#!/bin/bash

# Değişken tanımlama
PROJE_ADI="ComputerVision"
VERI_YOLU="/home/user/data"

# Değişken kullanma
echo "Proje: $PROJE_ADI"
echo "Veri yolu: ${VERI_YOLU}/images"
```

### 4. Fonksiyonlar

```bash
#!/bin/bash

# Fonksiyon tanımlama
print_header() {
    echo "================================"
    echo "$1"
    echo "================================"
}

# Fonksiyon çağırma
print_header 
```





## Kurulum Script'i Oluşturma

### Kapsamlı Kurulum Script'i Örneği

#### install.sh:
```bash
#!/bin/bash

# Script'in bulunduğu dizini al
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Modülleri yükle
source "$SCRIPT_DIR/scripts/common.sh"
source "$SCRIPT_DIR/scripts/dependencies.sh"
source "$SCRIPT_DIR/scripts/opencv.sh"
source "$SCRIPT_DIR/scripts/python_setup.sh"

# Konfigürasyonu yükle
source "$SCRIPT_DIR/config/settings.sh"

# Hata durumunda scripti durdur
set -e

# Trap ile temizlik işlemi
trap cleanup EXIT

cleanup() {
    log_info "Temizlik yapılıyor..."
}

# Banner göster
show_banner() {
    echo "========================================"
    echo "   Computer Vision Proje Kurulumu"
    echo "========================================"
    echo ""
}

# Kullanım bilgisi
usage() {
    echo "Kullanım: $0 [OPTIONS]"
    echo ""
    echo "Seçenekler:"
    echo "  -h, --help              Bu yardım mesajını göster"
    echo "  -f, --full              Tam kurulum (OpenCV dahil)"
    echo "  -q, --quick             Hızlı kurulum (sadece Python)"
    echo "  --skip-opencv           OpenCV kurulumunu atla"
    echo "  --cuda-version VERSION  CUDA versiyonu belirt (varsayılan: 12.1)"
    echo ""
    exit 1
}

# Komut satırı argümanlarını işle
FULL_INSTALL=false
QUICK_INSTALL=false
SKIP_OPENCV=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -f|--full)
            FULL_INSTALL=true
            shift
            ;;
        -q|--quick)
            QUICK_INSTALL=true
            shift
            ;;
        --skip-opencv)
            SKIP_OPENCV=true
            shift
            ;;
        --cuda-version)
            CUDA_VERSION="$2"
            shift 2
            ;;
        *)
            log_error "Bilinmeyen seçenek: $1"
            usage
            ;;
    esac
done

# Ana kurulum fonksiyonu
main() {
    show_banner
    
    # Sistem kontrolü
    check_root
    check_os
    
    # Kurulum tipine göre işle
    if [ "$QUICK_INSTALL" = true ]; then
        log_info "Hızlı kurulum başlatılıyor..."
        install_python_packages
    elif [ "$FULL_INSTALL" = true ]; then
        log_info "Tam kurulum başlatılıyor..."
        install_system_dependencies
        
        if [ "$SKIP_OPENCV" = false ]; then
            install_opencv_from_source
        fi
        
        install_python_packages
        setup_python_environment
    else
        log_info "Standart kurulum başlatılıyor..."
        install_system_dependencies
        install_python_packages
    fi
    
    # Kurulum sonrası kontroller
    verify_installation
    
    log_info "Kurulum başarıyla tamamlandı!"
}

# Kurulum doğrulama
verify_installation() {
    log_info "Kurulum doğrulanıyor..."
    
    # Python kontrol
    if command -v python3 &> /dev/null; then
        PYTHON_VER=$(python3 --version)
        log_info "Python: $PYTHON_VER ✓"
    else
        log_error "Python bulunamadı"
        return 1
    fi
    
    # OpenCV kontrol
    if python3 -c "import cv2" 2>/dev/null; then
        CV_VER=$(python3 -c "import cv2; print(cv2.__version__)")
        log_info "OpenCV: $CV_VER ✓"
    else
        log_warning "OpenCV Python binding bulunamadı"
    fi
    
    # PyTorch kontrol
    if python3 -c "import torch" 2>/dev/null; then
        TORCH_VER=$(python3 -c "import torch; print(torch.__version__)")
        log_info "PyTorch: $TORCH_VER ✓"
    else
        log_warning "PyTorch bulunamadı"
    fi
}

# Script'i çalıştır
main "$@"
```

### Python Sanal Ortam Kurulum Script'i

#### scripts/python_setup.sh:
```bash
#!/bin/bash

setup_python_environment() {
    local ENV_NAME="cv_env"
    local REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
    
    log_info "Python sanal ortamı oluşturuluyor..."
    
    # venv kur
    apt-get install -y python3-venv
    
    # Sanal ortam oluştur
    python3 -m venv "$PROJECT_ROOT/$ENV_NAME"
    
    # Aktive et
    source "$PROJECT_ROOT/$ENV_NAME/bin/activate"
    
    # Requirements kur
    if [ -f "$REQUIREMENTS_FILE" ]; then
        log_info "Requirements.txt'den paketler kuruluyor..."
        pip install -r "$REQUIREMENTS_FILE"
    fi
    
    # Aktivasyon script'i oluştur
    cat > "$PROJECT_ROOT/activate_env.sh" <<EOF
#!/bin/bash
source "$PROJECT_ROOT/$ENV_NAME/bin/activate"
echo "Python ortamı aktifleştirildi: $ENV_NAME"
EOF
    
    chmod +x "$PROJECT_ROOT/activate_env.sh"
    
    log_info "Python ortamı hazır: $PROJECT_ROOT/$ENV_NAME"
}
```

---

## Pratik Örnekler

### 1. Veri İşleme Pipeline Script'i

```bash
#!/bin/bash

# Konfigürasyon
INPUT_DIR="/data/raw"
OUTPUT_DIR="/data/processed"
LOG_FILE="processing.log"

# İşleme fonksiyonu
process_images() {
    local input_path="$1"
    local output_path="$2"
    
    echo "[$(date)] İşleniyor: $input_path" >> "$LOG_FILE"
    
    # Python script çağır
    python3 process_image.py \
        --input "$input_path" \
        --output "$output_path" \
        --resize 640,640 \
        --format jpg
    
    if [ $? -eq 0 ]; then
        echo "[$(date)] Başarılı: $input_path" >> "$LOG_FILE"
        return 0
    else
        echo "[$(date)] HATA: $input_path" >> "$LOG_FILE"
        return 1
    fi
}

# Ana döngü
main() {
    mkdir -p "$OUTPUT_DIR"
    
    # Tüm resimleri işle
    find "$INPUT_DIR" -type f \( -name "*.jpg" -o -name "*.png" \) | while read -r img; do
        filename=$(basename "$img")
        process_images "$img" "$OUTPUT_DIR/$filename"
    done
    
    echo "İşlem tamamlandı. Log: $LOG_FILE"
}

main "$@"
```

### 2. Model Eğitim Script'i

```bash
#!/bin/bash

# Eğitim parametreleri
MODEL_NAME="yolov11n"
DATASET_PATH="/data/dataset.yaml"
EPOCHS=100
BATCH_SIZE=16
IMAGE_SIZE=640

# GPU kontrolü
check_gpu() {
    if command -v nvidia-smi &> /dev/null; then
        echo "GPU bulundu:"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
        return 0
    else
        echo "GPU bulunamadı, CPU kullanılacak"
        return 1
    fi
}

# Eğitim başlat
train_model() {
    local experiment_name="exp_$(date +%Y%m%d_%H%M%S)"
    
    echo "Eğitim başlıyor: $experiment_name"
    
    python3 train.py \
        --model "$MODEL_NAME" \
        --data "$DATASET_PATH" \
        --epochs "$EPOCHS" \
        --batch "$BATCH_SIZE" \
        --imgsz "$IMAGE_SIZE" \
        --name "$experiment_name" \
        --device 0 \
        --workers 8 \
        --cache
    
    if [ $? -eq 0 ]; then
        echo "Eğitim tamamlandı: runs/detect/$experiment_name"
    else
        echo "Eğitim başarısız oldu!"
        exit 1
    fi
}

# Ana
main() {
    check_gpu
    train_model
}

main
```

### 3. Benchmark Script'i

```bash
#!/bin/bash

# Benchmark ayarları
MODELS=("yolov8n" "yolov8s" "yolov8m")
TEST_IMAGE="/data/test.jpg"
ITERATIONS=100

# Sonuç dosyası
RESULT_FILE="benchmark_results_$(date +%Y%m%d_%H%M%S).csv"

# Header yaz
echo "Model,Iteration,FPS,Inference_Time_ms,Memory_MB" > "$RESULT_FILE"

# Her model için test
for model in "${MODELS[@]}"; do
    echo "Testing $model..."
    
    for i in $(seq 1 $ITERATIONS); do
        # Python benchmark script'i çağır
        result=$(python3 benchmark.py --model "$model" --image "$TEST_IMAGE")
        echo "$model,$i,$result" >> "$RESULT_FILE"
        
        # İlerleme göster
        echo -ne "İlerleme: $i/$ITERATIONS\r"
    done
    
    echo ""
done

echo "Benchmark tamamlandı: $RESULT_FILE"

# Ortalama hesapla
python3 analyze_benchmark.py --input "$RESULT_FILE"
```

### 4. Toplu Video İşleme Script'i

```bash
#!/bin/bash

# Konfigürasyon
INPUT_DIR="/data/videos"
OUTPUT_DIR="/data/processed_videos"
MODEL="yolov11n.pt"
CONF_THRESHOLD=0.25

# Video işleme fonksiyonu
process_video() {
    local input_video="$1"
    local output_video="$2"
    
    echo "İşleniyor: $(basename "$input_video")"
    
    python3 detect_video.py \
        --source "$input_video" \
        --weights "$MODEL" \
        --output "$output_video" \
        --conf-thres "$CONF_THRESHOLD" \
        --save-txt \
        --save-conf
    
    if [ $? -eq 0 ]; then
        echo "✓ Tamamlandı: $(basename "$output_video")"
        return 0
    else
        echo "✗ Hata: $(basename "$input_video")"
        return 1
    fi
}

# Ana fonksiyon
main() {
    mkdir -p "$OUTPUT_DIR"
    
    # Video sayısını say
    video_count=$(find "$INPUT_DIR" -type f \( -name "*.mp4" -o -name "*.avi" \) | wc -l)
    echo "Toplam $video_count video bulundu"
    
    # Her video için
    current=0
    find "$INPUT_DIR" -type f \( -name "*.mp4" -o -name "*.avi" \) | while read -r video; do
        ((current++))
        filename=$(basename "$video")
        output_path="$OUTPUT_DIR/${filename%.*}_detected.mp4"
        
        echo "[$current/$video_count] İşleniyor..."
        process_video "$video" "$output_path"
    done
    
    echo "Tüm videolar işlendi!"
}

main "$@"
```

---

## İleri Seviye Konular

### 1. Hata Yönetimi

```bash
#!/bin/bash

# Exit on error
set -e

# Error handler
error_handler() {
    local line_num=$1
    echo "Error on line $line_num"
    cleanup
    exit 1
}

# Trap errors
trap 'error_handler $LINENO' ERR

# Cleanup fonksiyonu
cleanup() {
    echo "Cleaning up..."
    rm -rf /tmp/temp_files
}

# Exit'te cleanup çağır
trap cleanup EXIT

# Örnek kullanım
risky_operation() {
    # Hata olursa trap tetiklenecek
    cp /nonexistent/file /tmp/
}

risky_operation
```

### 2. Paralel İşleme

```bash
#!/bin/bash

# Paralel işlem sayısı
MAX_PARALLEL=4

# İş kuyruğu
process_queue() {
    local job_count=0
    
    for file in /data/*.jpg; do
        # Arka planda işle
        process_file "$file" &
        
        ((job_count++))
        
        # Max paralel işlem sayısına ulaşınca bekle
        if [ $job_count -ge $MAX_PARALLEL ]; then
            wait -n  # Bir işin bitmesini bekle
            ((job_count--))
        fi
    done
    
    # Kalan işleri bekle
    wait
    
    echo "Tüm işlemler tamamlandı"
}

process_file() {
    echo "Processing: $1"
    # Gerçek işlem burada
    python3 process.py "$1"
}

process_queue
```

### 3. Gelişmiş Loglama Sistemi

```bash
#!/bin/bash

# Log dizini
LOG_DIR="/var/log/cv_project"
mkdir -p "$LOG_DIR"

# Log dosyası
LOG_FILE="$LOG_DIR/install_$(date +%Y%m%d).log"

# Log seviyeleri
declare -A LOG_LEVELS=( [DEBUG]=0 [INFO]=1 [WARNING]=2 [ERROR]=3 [CRITICAL]=4 )
CURRENT_LOG_LEVEL=1  # INFO

# Log fonksiyonu
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Seviye kontrolü
    if [ ${LOG_LEVELS[$level]} -ge $CURRENT_LOG_LEVEL ]; then
        echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
    fi
}

# Kullanım örnekleri
log "DEBUG" "Detaylı debug bilgisi"
log "INFO" "Kurulum başlıyor"
log "WARNING" "Dikkat gerekiyor"
log "ERROR" "Bir hata oluştu"
log "CRITICAL" "Kritik hata!"

# Renkli log versiyonu
log_colored() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        DEBUG)   color='\033[0;36m' ;;  # Cyan
        INFO)    color='\033[0;32m' ;;  # Green
        WARNING) color='\033[1;33m' ;;  # Yellow
        ERROR)   color='\033[0;31m' ;;  # Red
        CRITICAL) color='\033[1;31m' ;; # Bold Red
        *) color='\033[0m' ;;
    esac
    
    local nc='\033[0m'
    
    if [ ${LOG_LEVELS[$level]} -ge $CURRENT_LOG_LEVEL ]; then
        echo -e "${color}[$timestamp] [$level]${nc} $message" | tee -a "$LOG_FILE"
    fi
}
```

### 4. Konfigürasyon Yönetimi

#### config/settings.sh:
```bash
#!/bin/bash

# Proje ayarları
export PROJECT_NAME="CV_Project"
export PROJECT_VERSION="1.0.0"

# Yol ayarları
export PROJECT_ROOT="/opt/cv_project"
export DATA_DIR="$PROJECT_ROOT/data"
export MODEL_DIR="$PROJECT_ROOT/models"
export LOG_DIR="$PROJECT_ROOT/logs"

# Python ayarları
export PYTHON_VERSION="3.10"
export VENV_NAME="cv_env"

# CUDA ayarları
export CUDA_VERSION="12.1"
export CUDNN_VERSION="8.9"

# Model ayarları
export DEFAULT_MODEL="yolov11n"
export DEFAULT_IMG_SIZE=640
export DEFAULT_CONF_THRESH=0.25

# Performans ayarları
export MAX_WORKERS=8
export BATCH_SIZE=16

# Dizin yapısını oluştur
create_project_structure() {
    local dirs=(
        "$DATA_DIR/raw"
        "$DATA_DIR/processed"
        "$DATA_DIR/annotations"
        "$MODEL_DIR/weights"
        "$MODEL_DIR/checkpoints"
        "$LOG_DIR"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
        echo "Created: $dir"
    done
}
```

### 5. Argüman Parse (getopt kullanımı)

```bash
#!/bin/bash

# Varsayılan değerler
VERBOSE=false
OUTPUT_DIR="./output"
MODEL="yolov11n"
DEVICE="0"

# Long options parse
TEMP=$(getopt -o hvd:m:o: --long help,verbose,device:,model:,output: -n 'script.sh' -- "$@")

if [ $? != 0 ]; then
    echo "Argüman hatası!" >&2
    exit 1
fi

eval set -- "$TEMP"

while true; do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--device)
            DEVICE="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "İç hata!"
            exit 1
            ;;
    esac
done

# Kalan argümanlar
INPUT_FILES="$@"

echo "Model: $MODEL"
echo "Device: $DEVICE"
echo "Output: $OUTPUT_DIR"
echo "Verbose: $VERBOSE"
echo "Input files: $INPUT_FILES"
```

### 6. Progress Bar

```bash
#!/bin/bash

# Progress bar fonksiyonu
show_progress() {
    local current=$1
    local total=$2
    local width=50
    
    local percent=$((current * 100 / total))
    local completed=$((width * current / total))
    local remaining=$((width - completed))
    
    printf "\rProgress: ["
    printf "%${completed}s" | tr ' ' '='
    printf "%${remaining}s" | tr ' ' '-'
    printf "] %d%% (%d/%d)" $percent $current $total
    
    if [ $current -eq $total ]; then
        echo ""
    fi
}

# Kullanım örneği
total_files=100
for i in $(seq 1 $total_files); do
    # Simüle edilmiş iş
    sleep 0.1
    show_progress $i $total_files
done
```

### 7. İnteraktif Menü

```bash
#!/bin/bash

# Menü göster
show_menu() {
    clear
    echo "================================"
    echo "    Computer Vision Araçları"
    echo "================================"
    echo "1. Veri İşle"
    echo "2. Model Eğit"
    echo "3. Inference Yap"
    echo "4. Benchmark Çalıştır"
    echo "5. Çıkış"
    echo "================================"
}

# Kullanıcı seçimini al
get_choice() {
    local choice
    read -p "Seçiminiz (1-5): " choice
    echo $choice
}

# Ana döngü
main_menu() {
    while true; do
        show_menu
        choice=$(get_choice)
        
        case $choice in
            1)
                echo "Veri işleniyor..."
                # process_data fonksiyonunu çağır
                ;;
            2)
                echo "Model eğitiliyor..."
                # train_model fonksiyonunu çağır
                ;;
            3)
                echo "Inference yapılıyor..."
                # run_inference fonksiyonunu çağır
                ;;
            4)
                echo "Benchmark çalıştırılıyor..."
                # run_benchmark fonksiyonunu çağır
                ;;
            5)
                echo "Çıkış yapılıyor..."
                exit 0
                ;;
            *)
                echo "Geçersiz seçim!"
                read -p "Devam etmek için Enter'a basın..."
                ;;
        esac
    done
}

main_menu
```

### 8. Dosya Kilitleme (Lock File)

```bash
#!/bin/bash

LOCK_FILE="/tmp/script.lock"

# Lock dosyası oluştur
acquire_lock() {
    if [ -f "$LOCK_FILE" ]; then
        local pid=$(cat "$LOCK_FILE")
        
        # Process hala çalışıyor mu?
        if kill -0 "$pid" 2>/dev/null; then
            echo "Script zaten çalışıyor (PID: $pid)"
            exit 1
        else
            echo "Eski lock dosyası temizleniyor..."
            rm -f "$LOCK_FILE"
        fi
    fi
    
    # Yeni lock oluştur
    echo $$ > "$LOCK_FILE"
}

# Lock dosyasını kaldır
release_lock() {
    rm -f "$LOCK_FILE"
}

# Trap ile temizlik
trap release_lock EXIT

# Lock'u al
acquire_lock

# Ana işlem
echo "Script çalışıyor..."
sleep 10
echo "Tamamlandı"
```

---

## Faydalı İpuçları ve Best Practices

### 1. Strict Mode Kullanımı

```bash
#!/bin/bash

# Hata durumunda dur
set -e

# Tanımsız değişken kullanımında dur
set -u

# Pipe'da hata durumunda dur
set -o pipefail

# Veya hepsini bir arada
set -euo pipefail
```

### 2. Script Şablonu (Production-Ready)

```bash
#!/bin/bash

################################################################################
# Script: example.sh
# Description: Script açıklaması
# Author: İsim
# Date: 2025-01-01
# Version: 1.0.0
################################################################################

# Strict mode
set -euo pipefail
IFS=$'\n\t'

# Script dizini ve ismi
readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="1.0.0"

# Renkler
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Log fonksiyonları
log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
log_debug() { [[ $VERBOSE == true ]] && echo -e "${BLUE}[DEBUG]${NC} $*"; }

# Varsayılan değişkenler
VERBOSE=false
DRY_RUN=false

# Kullanım bilgisi
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Computer Vision proje yönetim scripti

OPTIONS:
    -h, --help              Bu yardım mesajını göster
    -v, --verbose           Detaylı çıktı
    -d, --dry-run           Gerçek işlem yapma (test modu)
    -V, --version           Versiyon bilgisini göster
    
EXAMPLES:
    $SCRIPT_NAME --verbose
    $SCRIPT_NAME --dry-run

EOF
    exit 1
}

# Versiyon bilgisi
show_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
    exit 0
}

# Cleanup fonksiyonu
cleanup() {
    local exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        log_error "Script hata ile sonlandı (exit code: $exit_code)"
    else
        log_info "Script başarıyla tamamlandı"
    fi
    
    # Geçici dosyaları temizle
    [[ -d /tmp/script_temp ]] && rm -rf /tmp/script_temp
}

# Exit'te cleanup çağır
trap cleanup EXIT

# Gereksinim kontrolleri
check_requirements() {
    local required_commands=("python3" "git" "cmake")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Gerekli komut bulunamadı: $cmd"
            exit 1
        fi
    done
    
    log_info "Tüm gereksinimler karşılandı"
}

# Ana fonksiyon
main() {
    log_info "Script başlıyor..."
    
    # Gereksinimleri kontrol et
    check_requirements
    
    # Ana işlem burada
    if [ "$DRY_RUN" = true ]; then
        log_warning "DRY RUN modu - gerçek işlem yapılmıyor"
    fi
    
    log_info "İşlem tamamlandı"
}

# Argüman parse
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -V|--version)
            show_version
            ;;
        *)
            log_error "Bilinmeyen seçenek: $1"
            usage
            ;;
    esac
done

# Script'i çalıştır
main "$@"
```

### 3. Komut Varlık Kontrolü

```bash
#!/bin/bash

# Tek komut kontrolü
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 bulunamadı!"
        return 1
    fi
    return 0
}

# Çoklu komut kontrolü
check_commands() {
    local missing=()
    
    for cmd in "$@"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo "Eksik komutlar: ${missing[*]}"
        return 1
    fi
    
    return 0
}

# Kullanım
check_commands python3 git cmake gcc || exit 1
```

### 4. Timeout ile Komut Çalıştırma

```bash
#!/bin/bash

# Timeout ile komut çalıştır
run_with_timeout() {
    local timeout=$1
    shift
    local command=("$@")
    
    timeout "$timeout" "${command[@]}"
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "Komut timeout oldu: ${command[*]}"
        return 1
    fi
    
    return $exit_code
}

# Kullanım
run_with_timeout 30s python3 long_running_script.py
```

### 5. JSON Parse (jq kullanımı)

```bash
#!/bin/bash

# JSON dosyasından veri çek
parse_config() {
    local config_file="$1"
    
    if ! command -v jq &> /dev/null; then
        echo "jq bulunamadı, lütfen kurun"
        exit 1
    fi
    
    # JSON'dan değer oku
    MODEL=$(jq -r '.model.name' "$config_file")
    BATCH_SIZE=$(jq -r '.training.batch_size' "$config_file")
    EPOCHS=$(jq -r '.training.epochs' "$config_file")
    
    echo "Model: $MODEL"
    echo "Batch Size: $BATCH_SIZE"
    echo "Epochs: $EPOCHS"
}

# config.json örneği:
# {
#   "model": {
#     "name": "yolov11n"
#   },
#   "training": {
#     "batch_size": 16,
#     "epochs": 100
#   }
# }

parse_config "config.json"
```
```
## Sonuç

Bu rehber, shell script'leri kullanarak Computer Vision projeleriniz için:
- Modüler ve bakımı kolay kurulum sistemleri
- Otomatik veri işleme pipeline'ları
- Model eğitim ve test script'leri
- Benchmark ve performans ölçüm araçları


oluşturmanıza yardımcı olacaktır. Script'lerinizi her zaman temiz, okunabilir ve hata yönetimine dikkat ederek yazın.

