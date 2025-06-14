import os
from cryptography.fernet import Fernet
from stegano.embed import embed_text_in_image
from stegano.extract import extract_text_from_image

# Paths
image_input = "samples/input.jpeg"      # Make sure this exists
image_output_raw = "samples/output_raw.jpeg"
image_output_enc = "samples/output_enc.jpeg"

# Create sample message
message = "This is a secret test message!"

# --------- RAW (non-encrypted) embedding test ---------
print("\n=== RAW EMBED TEST ===")
embed_text_in_image(image_input, message, image_output_raw)
extracted_raw = extract_text_from_image(image_output_raw)
print("Extracted RAW:", extracted_raw)

# --------- ENCRYPTED embedding test ---------
print("\n=== ENCRYPTED EMBED TEST ===")
key = Fernet.generate_key()
embed_text_in_image(image_input, message, image_output_enc, encrypt=True, key=key)
extracted_enc = extract_text_from_image(image_output_enc, decrypt=True, key=key)
print("Extracted ENC:", extracted_enc)

# --------- Encrypted extract without key (should fail) ---------
print("\n=== ENCRYPTED EXTRACT WITHOUT KEY TEST ===")
try:
    extract_text_from_image(image_output_enc)  # No decryption
except Exception as e:
    print("Expected failure:", str(e))
