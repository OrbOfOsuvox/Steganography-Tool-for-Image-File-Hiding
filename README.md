# Steganography-Tool-for-Image-File-Hiding

# 🕵️‍♂️ Steganography Tool — Hide and Extract Text or Files in Images

A Python-based steganography tool with a Tkinter GUI that allows you to securely hide and extract messages (with optional encryption) in image files. Supports drag-and-drop, encryption using Fernet (PBKDF2-derived key), and JPEG-to-PNG conversion to preserve pixel integrity.

---

## 📦 Features

- 🔒 **Password-based Encryption** (Fernet/AES via PBKDF2)
- 🖼️ **Supports PNG, JPG, JPEG, BMP** (JPEGs are auto-converted to PNG)
- 🐭 **Drag & Drop Image Interface**
- 📐 **Image Metadata Preview** (size, dimensions)
- 🧠 **Automatic Detection of Encrypted vs Plain Text**
- 📁 **Save, Clear, Extract Functions**
- ✅ **Integrity Check for Hidden Messages**
- 🧪 **Test Scripts Included for Automation**
- 📦 **Export as Executable (.exe)**




💡 Credits
Developed with ❤️ using Python, NumPy, and Pillow

Cryptography powered by Fernet

GUI built using TkinterDnD2

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 🚀 Getting Started
### 🔧 Installation

Clone the repo:

```bash
git clone https://github.com/yourusername/steganography-tool.git
cd steganography-tool
```

Install dependencies:

```bash
pip install -r requirements.txt
```             
Note: If you get errors for numpy, Pillow, or cryptography, install them individually:
```bash
pip install numpy pillow cryptography tkinterdnd2
```

### ▶️ Run the App

```bash
python main.py    
```
The GUI will launch. Drag and drop an image, type a message, and click "Hide Message".

🛠️ Project Structure
```bash
steganography_tool/
│
├── gui/
│   └── app.py               # Main Tkinter GUI
│
├── stegano/
│   ├── embed.py             # Embeds text/file in image using LSB
│   ├── extract.py           # Extracts text/file from image
│
├── tests/
│   └── V2_test_steganography.py  # CLI test script
│
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
└── README.md
```

🔐 How It Works

Converts message to bits and embeds LSB into image.

Optionally encrypts message using Fernet + password.

Detects and decodes messages starting with:

ENC:: → Encrypted

TXT:: → Plaintext

JPEGs are automatically converted to PNG before embedding.

🧪 Testing
Run test script to embed/extract sample messages:
```bash
python V2_test_steganography.py
```

📦 Build as .exe (Windows)
Install PyInstaller:
```bash
pip install pyinstaller
```
Build:
```bash
pyinstaller --onefile --windowed main.py
```
Add a custom icon with --icon=icon.ico

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

💡 Credits

Developed with ❤️ using Python, NumPy, and Pillow

Cryptography powered by Fernet

GUI built using TkinterDnD2











