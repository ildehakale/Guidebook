from ultralytics import YOLO
import os

def train_yolo():
    """
    YOLO modeli eğitim scripti
    Dataset yapısı:
    dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    └── labels/
        ├── train/
        └── val/
    """
    
    # Model seçimi - yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    # Veya yolov11n.pt, yolov11s.pt gibi daha yeni versiyonlar
    model = YOLO('yolov8n.pt')  # nano model - en hızlı ama en düşük accuracy
    # model = YOLO('yolov8s.pt')  # small
    # model = YOLO('yolov8m.pt')  # medium
    # model = YOLO('yolov8l.pt')  # large
    # model = YOLO('yolov8x.pt')  # xlarge - en yavaş ama en yüksek accuracy
    
    # Eğitim parametreleri
    results = model.train(
        data='data.yaml',           # Dataset config dosyası (aşağıda açıklaması var)
        epochs=100,                 # Epoch sayısı
        imgsz=640,                  # Input image boyutu (640, 1024, 1280 gibi)
        batch=16,                   # Batch size (-1 otomatik batch size)
        
        # Opsiyonel parametreler:
        # device=0,                 # GPU device (0, 1, 2... veya 'cpu', [0,1] multi-gpu)
        # workers=8,                # DataLoader worker sayısı
        # project='runs/train',     # Sonuçların kaydedileceği klasör
        # name='exp',               # Deney adı
        # exist_ok=False,           # Varolan projeyi overwrite et
        # pretrained=True,          # Pretrained weights kullan
        # optimizer='auto',         # Optimizer seçimi ('SGD', 'Adam', 'AdamW', 'auto')
        # verbose=True,             # Detaylı log
        # seed=0,                   # Random seed
        # deterministic=True,       # Deterministic mode
        # single_cls=False,         # Tek sınıf eğitimi
        # rect=False,               # Rectangular training
        # cos_lr=False,             # Cosine learning rate scheduler
        # close_mosaic=10,          # Son N epoch'ta mosaic augmentation'ı kapat
        # resume=False,             # Son checkpoint'ten devam et
        # amp=True,                 # Automatic Mixed Precision
        # fraction=1.0,             # Dataset'in kullanılacak oranı (0.1 = %10)
        # profile=False,            # Profiler ONNX ve TensorRT speedleri
        
        # Hyperparameters:
        # lr0=0.01,                 # Initial learning rate
        # lrf=0.01,                 # Final learning rate (lr0 * lrf)
        # momentum=0.937,           # SGD momentum/Adam beta1
        # weight_decay=0.0005,      # Optimizer weight decay
        # warmup_epochs=3.0,        # Warmup epochs
        # warmup_momentum=0.8,      # Warmup initial momentum
        # warmup_bias_lr=0.1,       # Warmup initial bias lr
        # box=7.5,                  # Box loss gain
        # cls=0.5,                  # Cls loss gain
        # dfl=1.5,                  # DFL loss gain
        # pose=12.0,                # Pose loss gain (sadece pose estimation için)
        # kobj=2.0,                 # Keypoint obj loss gain
        # label_smoothing=0.0,      # Label smoothing epsilon
        # nbs=64,                   # Nominal batch size
        # hsv_h=0.015,              # HSV-Hue augmentation
        # hsv_s=0.7,                # HSV-Saturation augmentation
        # hsv_v=0.4,                # HSV-Value augmentation
        # degrees=0.0,              # Rotation augmentation (degrees)
        # translate=0.1,            # Translation augmentation
        # scale=0.5,                # Scale augmentation
        # shear=0.0,                # Shear augmentation (degrees)
        # perspective=0.0,          # Perspective augmentation
        # flipud=0.0,               # Vertical flip probability
        # fliplr=0.5,               # Horizontal flip probability
        # mosaic=1.0,               # Mosaic augmentation probability
        # mixup=0.0,                # Mixup augmentation probability
        # copy_paste=0.0,           # Copy-paste augmentation probability
        
        # Validation/Testing:
        # val=True,                 # Her epoch'ta validation yap
        # save=True,                # Checkpoint kaydet
        # save_period=-1,           # Her N epoch'ta kaydet (-1 = sadece son)
        # cache=False,              # Image'leri RAM'e cache'le ('ram' veya 'disk')
        # plots=True,               # Training plots kaydet
        # conf=0.25,                # Confidence threshold
        # iou=0.7,                  # NMS IoU threshold
        # max_det=300,              # Maximum detections per image
    )
    
    # Eğitim sonuçlarını göster
    print(f"Eğitim tamamlandı!")
    print(f"En iyi model: {results.save_dir}/weights/best.pt")


if __name__ == '__main__':
    train_yolo()




