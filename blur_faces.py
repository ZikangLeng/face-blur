#!/usr/bin/env python3
"""
blur_faces.py

Detects faces in images within a directory and applies a blur to each detected face.

Usage:
    python blur_faces.py --input_dir INPUT_DIR --output_dir OUTPUT_DIR [--blur_kernel KERNEL_WIDTH KERNEL_HEIGHT]
"""

import os
import argparse
from retinaface import RetinaFace
import cv2
from tqdm import tqdm

def detect_faces(image_path):
    """
    Detect faces in an image using RetinaFace.

    Args:
        image_path (str): Path to the input image.

    Returns:
        list of tuples: List of bounding boxes (x, y, width, height).
    """
    result = RetinaFace.detect_faces(image_path)
    bboxes = []
    if isinstance(result, tuple):
        # No faces detected
        return bboxes
    for face_data in result.values():
        x1, y1, x2, y2 = face_data["facial_area"]
        x = x1
        y = y1
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        bboxes.append((x, y, width, height))
    return bboxes

def blur_faces_in_image(image_path, output_path, blur_kernel=(50, 50)):
    """
    Detect and blur faces in a single image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the blurred image.
        blur_kernel (tuple): Kernel size for blurring (width, height).
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: unable to read {image_path}")
        return
    bboxes = detect_faces(image_path)
    for (x, y, w, h) in bboxes:
        roi = img[y:y+h, x:x+w]
        blurred_roi = cv2.blur(roi, blur_kernel)
        img[y:y+h, x:x+w] = blurred_roi
    cv2.imwrite(output_path, img)

def process_directory(input_dir, output_dir, blur_kernel=(50, 50), exts=None):
    """
    Process all images in a directory, blurring faces.

    Args:
        input_dir (str): Directory containing input images.
        output_dir (str): Directory to save blurred images.
        blur_kernel (tuple): Kernel size for blurring.
        exts (list): List of image file extensions to process.
    """
    if exts is None:
        exts = ['.jpg', '.jpeg', '.png']
    os.makedirs(output_dir, exist_ok=True)
    print(f"Processing {input_dir}...")
    for filename in tqdm(os.listdir(input_dir)):
        print(f"Processing {filename}...")
        name, ext = os.path.splitext(filename)
        if ext.lower() in exts:
            in_path = os.path.join(input_dir, filename)
            out_path = os.path.join(output_dir, filename)
            blur_faces_in_image(in_path, out_path, blur_kernel)

def parse_args():
    parser = argparse.ArgumentParser(description="Detect and blur faces in images")
    parser.add_argument('--input_dir', required=True, help="Directory with input images")
    parser.add_argument('--output_dir', required=True, help="Directory to save processed images")
    parser.add_argument('--blur_kernel', nargs=2, type=int, default=[50, 50],
                        metavar=('KERNEL_WIDTH','KERNEL_HEIGHT'),
                        help="Blurring kernel size, e.g. --blur_kernel 50 50")
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
    blur_kernel = tuple(args.blur_kernel)
    process_directory(args.input_dir, args.output_dir, blur_kernel)

if __name__ == '__main__':
    main()
