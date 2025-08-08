#!/usr/bin/env python3
"""
Example Usage of YOLOv8 Detector
Demonstrates various ways to use the detector
"""

from yolo_detector import YOLOv8Detector

def main():
    # Initialize detector
    detector = YOLOv8Detector("yolov8n.pt")
    
    print("=== Example 1: Detect from local file ===")
    # detector.detect_from_file("path/to/your/image.jpg")
    
    print("\n=== Example 2: Detect from URL ===")
    # Example URLs (you can replace with actual image URLs)
    example_urls = [
        "https://ultralytics.com/images/bus.jpg",
        "https://ultralytics.com/images/zidane.jpg"
    ]
    
    # Uncomment to test with actual URLs
    # for url in example_urls:
    #     detector.detect_from_url(url)
    
    print("\n=== Example 3: Detect from directory ===")
    # detector.detect_from_directory("path/to/image/directory")
    
    print("\n=== Example 4: Batch processing multiple URLs ===")
    # detector.detect_from_urls_batch(example_urls)
    
    print("\n=== Example 5: Real-time webcam detection ===")
    # Uncomment to use webcam (requires camera)
    # detector.detect_from_webcam()
    
    print("\n=== Example 6: Using the detector programmatically ===")
    
    # Example of using the detector in your own code
    class MyCustomDetector:
        def __init__(self):
            self.detector = YOLOv8Detector()
        
        def process_image_list(self, image_paths):
            """Process a list of images"""
            for path in image_paths:
                print(f"Processing: {path}")
                self.detector.detect_from_file(path, save_results=True)
        
        def process_url_list(self, urls):
            """Process a list of URLs"""
            for url in urls:
                print(f"Processing URL: {url}")
                self.detector.detect_from_url(url, save_results=True)
    
    # Example usage of custom detector
    # custom_detector = MyCustomDetector()
    # custom_detector.process_url_list(example_urls)
    
    print("\n=== Available Methods ===")
    print("1. detect_from_file(file_path)")
    print("2. detect_from_url(url)")
    print("3. detect_from_directory(dir_path)")
    print("4. detect_from_webcam(camera_index=0)")
    print("5. detect_from_urls_batch(url_list)")
    
    print("\n=== Command Line Usage Examples ===")
    print("python yolo_detector.py --source image.jpg")
    print("python yolo_detector.py --source https://example.com/image.jpg")
    print("python yolo_detector.py --dir /path/to/images")
    print("python yolo_detector.py --webcam")
    print("python yolo_detector.py --urls url1.jpg url2.jpg url3.jpg")
    print("python yolo_detector.py  # Interactive mode")

if __name__ == "__main__":
    main()