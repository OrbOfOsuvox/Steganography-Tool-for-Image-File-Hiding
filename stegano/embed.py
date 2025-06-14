from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import base64

def embed_text_in_image(image_path, message, output_path, encrypt=False, key=None):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)

    if encrypt:
        if not key:
            raise ValueError("Encryption key is required for encryption.")
        f = Fernet(key)
        encrypted_bytes = f.encrypt(message.encode())
        encrypted_b64 = base64.b64encode(encrypted_bytes).decode()
        full_message = "ENC::" + encrypted_b64
    else:
        full_message = "TXT::" + message

    binary_message = ''.join([format(ord(c), '08b') for c in full_message]) + '00000000'

    flat_pixels = pixels.reshape(-1, 3)
    total_bits = len(binary_message)

    if total_bits > flat_pixels.shape[0] * 3:
        raise ValueError("Message is too large to embed in the image.")

    bit_idx = 0
    for i in range(flat_pixels.shape[0]):
        for j in range(3):
            if bit_idx >= total_bits:
                break
            bit = int(binary_message[bit_idx])
            flat_pixels[i][j] = (flat_pixels[i][j] & 0b11111110) | bit
            bit_idx += 1

    # Reshape and clip pixel values, then convert to uint8
    stego_pixels = flat_pixels.reshape(pixels.shape)
    stego_pixels = np.clip(stego_pixels, 0, 255).astype(np.uint8)

    result_img = Image.fromarray(stego_pixels)
    result_img.save(output_path, format='PNG')

    print(f"Bits embedded: {bit_idx}/{total_bits}")
    print(f"Saving to: {output_path}")
