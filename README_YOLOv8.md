# YOLOv8 Object Detection Script

ระบบตรวจจับวัตถุด้วย YOLOv8 ที่รองรับการดึงภาพจากหลายแหล่งที่มาอย่างง่ายดาย

## คุณสมบัติ (Features)

- ✅ ตรวจจับวัตถุจากไฟล์ภาพในเครื่อง
- ✅ ดาวน์โหลดและตรวจจับภาพจาก URL
- ✅ ประมวลผลภาพทั้งโฟลเดอร์
- ✅ การตรวจจับแบบเรียลไทม์จากกล้องเว็บแคม
- ✅ ประมวลผล URL หลายรายการพร้อมกัน
- ✅ บันทึกผลลัพธ์พร้อมกรอบและป้ายกำกับ
- ✅ รองรับรูปแบบภาพหลากหลาย (JPG, PNG, BMP, TIFF, WebP)

## การติดตั้ง (Installation)

1. **ติดตั้ง dependencies:**
```bash
pip install -r requirements.txt
```

2. **โมเดล YOLOv8n จะดาวน์โหลดอัตโนมัติในการรันครั้งแรก**

## วิธีใช้งาน (Usage)

### 1. โหมดโต้ตอบ (Interactive Mode)
```bash
python yolo_detector.py
```

### 2. ตรวจจับจากไฟล์เดียว (Single File)
```bash
python yolo_detector.py --source path/to/image.jpg
```

### 3. ตรวจจับจาก URL
```bash
python yolo_detector.py --source https://example.com/image.jpg
```

### 4. ตรวจจับจากโฟลเดอร์ทั้งหมด (Directory)
```bash
python yolo_detector.py --dir path/to/images/
```

### 5. ตรวจจับจากกล้องเว็บแคม (Webcam)
```bash
python yolo_detector.py --webcam
```

### 6. ตรวจจับจาก URL หลายรายการ (Multiple URLs)
```bash
python yolo_detector.py --urls https://example1.com/img1.jpg https://example2.com/img2.jpg
```

### 7. ตัวเลือกเพิ่มเติม (Additional Options)
```bash
# ใช้โมเดลอื่น
python yolo_detector.py --model yolov8s.pt --source image.jpg

# เปลี่ยนโฟลเดอร์ผลลัพธ์
python yolo_detector.py --source image.jpg --output-dir my_results

# ไม่บันทึกผลลัพธ์
python yolo_detector.py --source image.jpg --no-save

# ใช้กล้องอื่น
python yolo_detector.py --webcam --camera-index 1
```

## การใช้งานในโค้ด Python (Programmatic Usage)

```python
from yolo_detector import YOLOv8Detector

# สร้าง detector
detector = YOLOv8Detector("yolov8n.pt")

# ตรวจจับจากไฟล์
detector.detect_from_file("image.jpg")

# ตรวจจับจาก URL
detector.detect_from_url("https://example.com/image.jpg")

# ตรวจจับจากโฟลเดอร์
detector.detect_from_directory("images/")

# ตรวจจับจาก URLs หลายรายการ
urls = ["url1.jpg", "url2.jpg", "url3.jpg"]
detector.detect_from_urls_batch(urls)

# ตรวจจับจากกล้อง
detector.detect_from_webcam()
```

## โครงสร้างไฟล์ (File Structure)

```
├── yolo_detector.py      # สคริปต์หลัก
├── requirements.txt      # dependencies
├── example_usage.py      # ตัวอย่างการใช้งาน
├── README_YOLOv8.md     # เอกสารนี้
└── results/             # โฟลเดอร์ผลลัพธ์ (สร้างอัตโนมัติ)
    ├── image1_detected.jpg
    ├── image2_detected.jpg
    └── ...
```

## ตัวอย่างผลลัพธ์ (Output Example)

```
Loading YOLOv8 model: yolov8n.pt
Model loaded successfully!
Processing file: example.jpg

--- Detection Results for: example.jpg ---
Detected: person (confidence: 0.89)
Detected: car (confidence: 0.76)
Detected: bicycle (confidence: 0.65)
--------------------------------------------------
Saved annotated image: results/example_detected.jpg
```

## รูปแบบภาพที่รองรับ (Supported Image Formats)

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## คลาสวัตถุที่ YOLOv8n สามารถตรวจจับได้

YOLOv8n ตรวจจับวัตถุ 80 ประเภทจาก COCO dataset:
- คน (person)
- ยานพาหนะ (bicycle, car, motorcycle, airplane, bus, train, truck, boat)
- สัตว์ (bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe)
- วัตถุในบ้าน (chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, scissors, teddy bear, hair drier, toothbrush)
- อาหาร (banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake)
- กีฬา (frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket)
- และอื่นๆ

## การแก้ไขปัญหา (Troubleshooting)

### ปัญหา: ไม่สามารถเปิดกล้องได้
```
Error: Could not open camera 0
```
**วิธีแก้:** ลองเปลี่ยน camera index หรือตรวจสอบว่ากล้องถูกใช้งานโดยแอปอื่นหรือไม่

### ปัญหา: ดาวน์โหลด URL ไม่ได้
```
Error processing URL: ...
```
**วิธีแก้:** ตรวจสอบ URL และการเชื่อมต่ออินเทอร์เน็ต

### ปัญหา: ไม่พบไฟล์
```
Error: File path/to/image.jpg not found!
```
**วิธีแก้:** ตรวจสอบ path ของไฟล์ให้ถูกต้อง

## ขั้นสูง (Advanced Usage)

### การใช้โมเดลอื่น
```python
# ใช้โมเดลที่แม่นยำกว่า
detector = YOLOv8Detector("yolov8s.pt")  # Small
detector = YOLOv8Detector("yolov8m.pt")  # Medium
detector = YOLOv8Detector("yolov8l.pt")  # Large
detector = YOLOv8Detector("yolov8x.pt")  # Extra Large
```

### การปรับแต่งการบันทึก
```python
# ไม่บันทึกผลลัพธ์
detector.detect_from_file("image.jpg", save_results=False)

# เปลี่ยนโฟลเดอร์ผลลัพธ์
detector.detect_from_file("image.jpg", output_dir="my_results")
```

## ใบอนุญาต (License)

โค้ดนี้ใช้ภายใต้ MIT License