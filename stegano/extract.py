from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import base64

def extract_text_from_image(image_path, decrypt=False, key=None):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    flat_pixels = pixels.reshape(-1, 3)

    bits = ""
    for pixel in flat_pixels:
        for channel in range(3):
            bits += str(pixel[channel] & 1)

    # Convert bits to characters
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            break
        byte_val = int(byte, 2)
        bytes_list.append(byte_val)
        if byte_val == 0:
            break  # End marker

    try:
        raw_data = bytes(bytes_list).decode(errors='ignore')
        message = raw_data.strip("\x00")  # Remove any padding null characters
    except Exception as e:
        raise ValueError("Failed to decode extracted data.") from e

    if message.startswith("ENC::"):
        if not decrypt or not key:
            raise ValueError("Encrypted message found but decryption key not provided.")
        try:
            encrypted_b64 = message[5:]
            decrypted = Fernet(key).decrypt(base64.b64decode(encrypted_b64))
            return decrypted.decode()
        except Exception as e:
            raise ValueError("Decryption failed.") from e

    elif message.startswith("TXT::"):
        return message[5:]

    else:
        raise ValueError("Unknown message format or corrupted data.")
