#!/usr/bin/env python3
"""
YOLOv8 Object Detection Script
Supports multiple image sources: local files, URLs, webcam, directories
"""

import os
import cv2
import requests
import argparse
import numpy as np
from pathlib import Path
from typing import List, Union, Optional
from ultralytics import YOLO
import urllib.parse
from PIL import Image
import io

class YOLOv8Detector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        """
        Initialize YOLOv8 detector
        
        Args:
            model_path: Path to YOLOv8 model file
        """
        print(f"Loading YOLOv8 model: {model_path}")
        self.model = YOLO(model_path)
        print("Model loaded successfully!")
    
    def detect_from_file(self, file_path: str, save_results: bool = True, output_dir: str = "results") -> None:
        """
        Detect objects in a single image file
        
        Args:
            file_path: Path to image file
            save_results: Whether to save detection results
            output_dir: Directory to save results
        """
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found!")
            return
        
        print(f"Processing file: {file_path}")
        results = self.model(file_path)
        
        if save_results:
            os.makedirs(output_dir, exist_ok=True)
            self._save_results(results, file_path, output_dir)
        
        self._print_detections(results, file_path)
    
    def detect_from_url(self, url: str, save_results: bool = True, output_dir: str = "results") -> None:
        """
        Detect objects in an image from URL
        
        Args:
            url: URL of the image
            save_results: Whether to save detection results
            output_dir: Directory to save results
        """
        try:
            print(f"Downloading image from: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Convert to PIL Image and then to numpy array
            image = Image.open(io.BytesIO(response.content))
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            results = self.model(image_np)
            
            if save_results:
                os.makedirs(output_dir, exist_ok=True)
                # Save original image and results
                filename = os.path.basename(urllib.parse.urlparse(url).path) or "url_image.jpg"
                self._save_results(results, filename, output_dir)
            
            self._print_detections(results, url)
            
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    
    def detect_from_directory(self, dir_path: str, save_results: bool = True, output_dir: str = "results") -> None:
        """
        Detect objects in all images in a directory
        
        Args:
            dir_path: Path to directory containing images
            save_results: Whether to save detection results
            output_dir: Directory to save results
        """
        if not os.path.exists(dir_path):
            print(f"Error: Directory {dir_path} not found!")
            return
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        
        image_files = []
        for ext in image_extensions:
            image_files.extend(Path(dir_path).glob(f"*{ext}"))
            image_files.extend(Path(dir_path).glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"No image files found in {dir_path}")
            return
        
        print(f"Found {len(image_files)} images in {dir_path}")
        
        for image_file in image_files:
            self.detect_from_file(str(image_file), save_results, output_dir)
    
    def detect_from_webcam(self, camera_index: int = 0, save_results: bool = False, output_dir: str = "results") -> None:
        """
        Real-time object detection from webcam
        
        Args:
            camera_index: Camera index (usually 0 for default camera)
            save_results: Whether to save detection results
            output_dir: Directory to save results
        """
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
        
        print("Press 'q' to quit, 's' to save current frame")
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Run inference
            results = self.model(frame)
            
            # Draw results on frame
            annotated_frame = results[0].plot()
            
            # Display frame
            cv2.imshow('YOLOv8 Detection', annotated_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and save_results:
                # Save current frame
                os.makedirs(output_dir, exist_ok=True)
                filename = f"webcam_frame_{frame_count:04d}.jpg"
                cv2.imwrite(os.path.join(output_dir, filename), annotated_frame)
                print(f"Saved frame: {filename}")
                frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
    
    def detect_from_urls_batch(self, urls: List[str], save_results: bool = True, output_dir: str = "results") -> None:
        """
        Detect objects in multiple images from URLs
        
        Args:
            urls: List of image URLs
            save_results: Whether to save detection results
            output_dir: Directory to save results
        """
        for i, url in enumerate(urls):
            print(f"\nProcessing URL {i+1}/{len(urls)}")
            self.detect_from_url(url, save_results, output_dir)
    
    def _save_results(self, results, source_name: str, output_dir: str) -> None:
        """Save detection results to files"""
        for i, result in enumerate(results):
            # Save annotated image
            filename = os.path.splitext(os.path.basename(source_name))[0]
            output_path = os.path.join(output_dir, f"{filename}_detected.jpg")
            result.save(output_path)
            print(f"Saved annotated image: {output_path}")
    
    def _print_detections(self, results, source: str) -> None:
        """Print detection results to console"""
        print(f"\n--- Detection Results for: {source} ---")
        for result in results:
            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = self.model.names[class_id]
                    print(f"Detected: {class_name} (confidence: {confidence:.2f})")
            else:
                print("No objects detected")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Object Detection with Multiple Sources")
    parser.add_argument("--model", default="yolov8n.pt", help="Path to YOLOv8 model")
    parser.add_argument("--source", help="Source: file path, URL, directory, or 'webcam'")
    parser.add_argument("--urls", nargs='+', help="List of image URLs")
    parser.add_argument("--dir", help="Directory containing images")
    parser.add_argument("--webcam", action="store_true", help="Use webcam")
    parser.add_argument("--camera-index", type=int, default=0, help="Camera index for webcam")
    parser.add_argument("--output-dir", default="results", help="Output directory for results")
    parser.add_argument("--no-save", action="store_true", help="Don't save results")
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = YOLOv8Detector(args.model)
    save_results = not args.no_save
    
    # Determine source type and run detection
    if args.webcam:
        detector.detect_from_webcam(args.camera_index, save_results, args.output_dir)
    elif args.urls:
        detector.detect_from_urls_batch(args.urls, save_results, args.output_dir)
    elif args.dir:
        detector.detect_from_directory(args.dir, save_results, args.output_dir)
    elif args.source:
        if args.source.startswith(('http://', 'https://')):
            detector.detect_from_url(args.source, save_results, args.output_dir)
        elif os.path.isfile(args.source):
            detector.detect_from_file(args.source, save_results, args.output_dir)
        elif os.path.isdir(args.source):
            detector.detect_from_directory(args.source, save_results, args.output_dir)
        else:
            print(f"Error: Source '{args.source}' not found or invalid")
    else:
        # Interactive mode
        print("\n=== YOLOv8 Object Detection ===")
        print("Choose an option:")
        print("1. Detect from local file")
        print("2. Detect from URL")
        print("3. Detect from directory")
        print("4. Detect from webcam")
        print("5. Detect from multiple URLs")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            file_path = input("Enter image file path: ").strip()
            detector.detect_from_file(file_path, save_results, args.output_dir)
        elif choice == "2":
            url = input("Enter image URL: ").strip()
            detector.detect_from_url(url, save_results, args.output_dir)
        elif choice == "3":
            dir_path = input("Enter directory path: ").strip()
            detector.detect_from_directory(dir_path, save_results, args.output_dir)
        elif choice == "4":
            detector.detect_from_webcam(args.camera_index, save_results, args.output_dir)
        elif choice == "5":
            print("Enter URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            if urls:
                detector.detect_from_urls_batch(urls, save_results, args.output_dir)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()