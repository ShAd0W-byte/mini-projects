# File Cipher

A small Python cryptography project that implements file encryption and decryption using classical Vigenère cipher for text files and repeating-key XOR for binary files.

## Features

* Encrypt and decrypt text files using Vigenère cipher
* Preserve uppercase and lowercase characters
* Leave non-alphabetic characters unchanged
* Encrypt and decrypt binary files such as ZIPs, PDFs, and images using XOR
* Uses a repeating key for binary encryption
* Supports both encryption and decryption through a simple command-line interface

## Usage

Run the program:

```bash
python3 file_cipher.py
```

Choose:

```text
T → Text file
N → Non-text/binary file

E → Encrypt
D → Decrypt
```

Example:

```text
Enter file type: text file [T] or non-text file [N]: T
For encrypt [E] or decrypt [D]: E
Enter input file: input.txt
Enter output file: encrypted.txt
Enter key: cyber
```

For binary files, the same interface is used. The file is read as raw bytes and each byte is XORed with a repeating key.

## Implementation

### Text Files

Uses the Vigenère cipher:

```text
Encryption: (text + key) % 26
Decryption: (text - key) % 26
```

### Binary Files

Uses repeating-key XOR:

```text
encrypted_byte = original_byte ^ key_byte
```

Applying XOR with the same key again reverses the operation:

```text
original_byte = encrypted_byte ^ key_byte
```

## Verification

The project was tested by encrypting and decrypting both text and binary files. After decryption, the resulting file should be identical to the original file.

## Technologies

* Python 3
* `re`
* File handling
* Vigenère Cipher
* XOR
* Binary file handling

## Note

This project is intended for educational purposes to demonstrate basic cryptography and Python file handling. Vigenère cipher and repeating-key XOR are **not suitable for protecting sensitive data in real-world applications**.
