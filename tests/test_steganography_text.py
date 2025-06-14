# test_steganography_text.py

from stegano.embed import embed_text_in_image
from stegano.extract import extract_text_from_image
from utils.crypto import generate_key
from PIL import Image

# Create a simple blank image to test with
def create_test_image(path):
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    img.save(path)

def run_text_stego_test():
    image_path = "test_input.png"
    stego_path = "test_output.png"
    message = "abc"

    # Optional: Encryption
    use_encryption = False
    key = generate_key() if use_encryption else None

    # Step 1: Create test image
    create_test_image(image_path)

    # Step 2: Embed message
    embed_text_in_image(image_path, message, stego_path, encrypt=use_encryption, key=key)

    # Step 3: Extract message
    extracted = extract_text_from_image(stego_path, decrypt=use_encryption, key=key)

    print(f"Original Message : {message}")
    print(f"Extracted Message: {extracted}")

if __name__ == "__main__":
    run_text_stego_test()
