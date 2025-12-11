# Loglama fonksiyonları
log_info() {
    echo -e "[INFO] $1"
}

log_success() {
    echo -e "[SUCCESS] $1"
}

log_warning() {
    echo -e "[WARNING] $1"
}

log_error() {
    echo -e "[ERROR] $1"
}

log_step() {
    echo -e "[STEP] $1"
}

#================================================================
# main function
main() {
    echo ""
    log_info "========================================"
    log_info "KURULUM"
    log_info "========================================"

    echo ""

    log_warning "Kurulum şimdi başlayacak"
    log_info "Tüm paketler kullanıcı dizinine kurulacaktır"
    log_info "Herhangi bir paket bulunamazsa, kurulum atlanacaktır."
    
    fonksiyon1
    fonksiyon2
    fonksiyon3 

    echo ""
    log_success "========================================"
    log_success "Kurulum Tamamlandı!"
    log_success "========================================"
    echo ""

}

# run main function 
main

#================================================================
# Örnek fonksiyon

# PyTorch'u kur
install_pytorch() {
    log_step "PyTorch wheel dosyasından kuruluyor..."
    
    cd "$INSTALL_DIR"
    
    # PyTorch wheel dosyasını bul
    TORCH_WHL=$(find . -maxdepth 1 -name "torch-*.whl" | head -n 1)
    
    if [ -z "$TORCH_WHL" ]; then
        log_error "PyTorch wheel dosyası bulunamadı! (torch-*.whl)"
        log_error "Lütfen $INSTALL_DIR içine yerleştirin. Kurulum atlanıyor."
    else
        log_info "Bulunan PyTorch wheel dosyası: $TORCH_WHL"
        log_info "PyTorch kuruluyor..."
        
        pip3 install --user "$TORCH_WHL"
        
        log_success "PyTorch kuruldu"
    fi
    echo ""
}

#================================================================




