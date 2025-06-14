import unittest
import os
from stegano import embed, extract
from utils.crypto import generate_key
from PIL import Image

class TestSteganography(unittest.TestCase):

    def setUp(self):
        self.text = "TestMessage"
        self.input_image = "test_input.png"
        self.stego_image = "test_output.png"
        self.test_file = "test_file.txt"
        self.extracted_file = "extracted_file.txt"

        # Create blank test image
        img = Image.new("RGB", (200, 200), color=(255, 255, 255))
        img.save(self.input_image)

        # Create test file
        with open(self.test_file, "w") as f:
            f.write(self.text)

    def tearDown(self):
        for f in [self.input_image, self.stego_image, self.test_file, self.extracted_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_text_embed_and_extract(self):
        embed.embed_text_in_image(self.input_image, self.text, self.stego_image)
        extracted = extract.extract_text_from_image(self.stego_image)
        self.assertEqual(self.text, extracted)

    def test_file_embed_and_extract(self):
        embed.embed_file_in_image(self.input_image, self.test_file, self.stego_image)
        extract.extract_file_from_image(self.stego_image, self.extracted_file)

        with open(self.test_file, "r") as original, open(self.extracted_file, "r") as extracted:
            self.assertEqual(original.read(), extracted.read())

    def test_encrypted_text_embed_and_extract(self):
        key = generate_key()
        embed.embed_text_in_image(self.input_image, self.text, self.stego_image, encrypt=True, key=key)
        extracted = extract.extract_text_from_image(self.stego_image, decrypt=True, key=key)
        self.assertEqual(self.text, extracted)

    def test_image_capacity_too_small(self):
        small_img_path = "small.png"
        img = Image.new("RGB", (5, 5), color=(255, 255, 255))  # Tiny image
        img.save(small_img_path)

        large_text = "A" * 5000  # Too much data

        with self.assertRaises(ValueError):
            embed.embed_text_in_image(small_img_path, large_text, self.stego_image)

        os.remove(small_img_path)

if __name__ == '__main__':
    unittest.main()
