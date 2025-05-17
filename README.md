# Face Blurring Script

This script detects faces in images using RetinaFace and applies a blur to each detected face.

## Installation

1. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python blur_faces.py --input_dir path/to/input/images --output_dir path/to/output/images [--blur_kernel 50 50]
```

- `--input_dir`: Directory containing the images to process.
- `--output_dir`: Directory where blurred images will be saved.
- `--blur_kernel`: (Optional) Two integers for the blurring kernel size (width height). Default is `50 50`.

## Example

```bash
python blur_faces.py --input_dir ./images --output_dir ./blurred_images --blur_kernel 100 100
```
