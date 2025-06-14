from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk, Image
import time
import sys

# Derive encryption key from password
def derive_key_from_password(password: str) -> bytes:
    salt = b"static_salt_12345678"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)

# Append app path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stegano.embed import embed_text_in_image
from stegano.extract import extract_text_from_image

# GUI App
class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("800x600")

        self.image_path = None
        self.output_path = None
        self.image_label = None

        self.drop_frame = tk.Label(self.root, text="Drop Image Here", relief=tk.RIDGE, width=80, height=10)
        self.drop_frame.pack(pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)

        self.image_info_frame = tk.Frame(self.root)
        self.image_info_frame.pack(pady=5)

        self.add_image_button = tk.Button(self.image_info_frame, text="Add Image", command=self.browse_image)
        self.add_image_button.pack(side=tk.LEFT)

        self.image_info_label = tk.Label(self.image_info_frame, text="", fg="green", font=("Arial", 10, "bold"))
        self.image_info_label.pack(side=tk.LEFT, padx=10)

        self.text_input = tk.Text(self.root, height=10)
        self.text_input.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Hide Message", command=self.hide_message).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Extract Message", command=self.extract_message).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Save Stego Image", command=self.save_image).pack(side=tk.LEFT, padx=10)

        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(self.root, text="", fg="blue", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=5)

    def update_status(self, message, color="blue"):
        self.status_label.config(text=message, fg=color)

    def load_image(self, path):
        if os.path.isfile(path) and path.lower().endswith(('png', 'jpg', 'jpeg', 'bmp')):
            ext = os.path.splitext(path)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                # Auto-convert JPEG to PNG
                img = Image.open(path).convert("RGB")
                base = os.path.splitext(os.path.basename(path))[0]
                converted_path = os.path.join(os.path.dirname(path), f"{base}_converted.png")
                img.save(converted_path, format="PNG")
                self.image_path = converted_path
                converted = True
            else:
                self.image_path = path
                converted = False

            # Update image info
            img = Image.open(self.image_path)
            width, height = img.size
            file_size_kb = os.path.getsize(self.image_path) / 1024
            filename = os.path.basename(self.image_path)

            self.image_info_label.config(
                text=f"✅ {filename} ({width}x{height}px, {file_size_kb:.1f} KB)"
            )
            self.status_var.set(f"Image loaded: {filename} | Size: {file_size_kb:.1f} KB | {width}x{height}px")

            # Show in preview area (optional)
            preview_img = ImageTk.PhotoImage(img.resize((300, 300)))
            if self.image_label:
                self.image_label.destroy()
            self.image_label = tk.Label(self.drop_frame, image=preview_img)
            self.image_label.image = preview_img
            self.image_label.pack()

            msg = f"{filename} has been added{' (converted from JPG)' if converted else ''} for steganography."
            messagebox.showinfo("Image Added", msg)
        else:
            messagebox.showerror("Invalid File", "Please select a valid image file.")

    def on_drop(self, event):
        path = event.data.strip('{}')
        self.load_image(path)

    def browse_image(self):
        filetypes = (("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*"))
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            if self.image_label:
                self.image_label.destroy()
                self.image_label = None
            self.load_image(filepath)

    def hide_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please drop or add an image first.")
            return

        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Message", "Please enter a message to hide.")
            return

        encrypt = messagebox.askyesno("Encrypt?", "Do you want to encrypt the message before embedding?")

        key_bytes = None
        if encrypt:
            password = simpledialog.askstring("Encryption Password", "Enter a password for encryption:", show="*")
            if not password:
                messagebox.showerror("Encryption Error", "Encryption password was not provided.")
                return
            try:
                key_bytes = derive_key_from_password(password)
            except Exception as e:
                messagebox.showerror("Key Error", f"Failed to derive key: {e}")
                return

        # Let user choose output path
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Stego Image As"
        )
        if not path:
            messagebox.showinfo("Cancelled", "Save location not selected. Aborting.")
            return

        self.output_path = path

        try:
            embed_text_in_image(
                self.image_path,
                text,
                self.output_path,
                encrypt=encrypt,
                key=key_bytes
            )
            messagebox.showinfo("Success", f"Message embedded into:\n{self.output_path}")
            self.status_var.set(f"Saved stego image at: {self.output_path}")
        except Exception as e:
            messagebox.showerror("Embedding Failed", str(e))
            self.update_status("Embedding failed.", color="red")

    def extract_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please drop or add an image first.")
            return

        try:
            # First attempt extraction without decryption
            extracted = extract_text_from_image(self.image_path)
            
            # Check if looks encrypted (rough check)
            if extracted.startswith("gAAAAA"):
                raise ValueError("Encrypted content detected")

        except Exception:
            # Ask for password
            answer = messagebox.askyesno("Encrypted?", "The message may be encrypted. Enter a password to decrypt?")
            if not answer:
                messagebox.showinfo("Encrypted", "Decryption skipped.")
                return

            password = simpledialog.askstring("Password", "Enter decryption password:", show="*")
            if not password:
                messagebox.showerror("No Password", "You must enter a password to decrypt the message.")
                return

            try:
                key_bytes = derive_key_from_password(password)
                extracted = extract_text_from_image(self.image_path, decrypt=True, key=key_bytes)
            except Exception as e:
                messagebox.showerror("Decryption Failed", f"Could not decrypt: {e}")
                return

        # Display the extracted message
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert(tk.END, extracted)

    def clear_all(self):
        self.text_input.delete("1.0", tk.END)

        if self.image_label:
            self.image_label.destroy()
            self.image_label = None

        self.image_path = None
        self.output_path = None
        self.image_info_label.config(text="")
        self.status_var.set("Cleared all fields.")

    def save_image(self):
        if not self.output_path or not os.path.exists(self.output_path):
            messagebox.showerror("Error", "No stego image to save.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            try:
                img = Image.open(self.output_path)
                img.save(path, format="PNG")
                messagebox.showinfo("Saved", f"Stego image saved to {path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save stego image.\n{e}")

if __name__ == '__main__':
    root = TkinterDnD.Tk()
    app = StegApp(root)
    root.mainloop()
