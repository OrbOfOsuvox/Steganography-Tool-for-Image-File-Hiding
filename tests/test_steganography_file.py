# test_steganography_file.py

from stegano.embed import embed_file_in_image
from stegano.extract import extract_file_from_image
from PIL import Image
import os

def create_sample_txt(path):
    with open(path, "w") as f:
        f.write("Secret text inside file!")

def run_file_stego_test():
    original_file = "sample.txt"
    image_path = "carrier.png"
    stego_path = "stego_image.png"
    output_file = "extracted_output.txt"

    # Step 1: Create test file and image
    create_sample_txt(original_file)
    Image.new("RGB", (200, 200), color=(255, 255, 255)).save(image_path)

    # Step 2: Embed file
    embed_file_in_image(image_path, original_file, stego_path)

    # Step 3: Extract back
    extract_file_from_image(stego_path, output_file)

    print("✅ File embedding and extraction complete.")
    print(f"Extracted content: {open(output_file).read()}")

if __name__ == "__main__":
    run_file_stego_test()
