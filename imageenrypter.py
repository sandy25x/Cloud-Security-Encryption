import os
from cryptography.hazmat.primitives.asymmetric import rsa
import tkinter as tk
from tkinter import filedialog
import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import sys
from PIL import Image

def generate_aes_key():
    return os.urandom(32)  # 256 bits for AES-256

def select_image():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    return file_path



def encrypt_aes_key(aes_key, rsa_public_key):   #aes key encryption with rsa private key 
    encrypted_key = rsa_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_key).decode('utf-8')

def encrypt_with_aes_ctr(image_path, aes_key): 
    with open(image_path, 'rb') as file:
        data = file.read()

    # Use Counter mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    encrypted_image_path = f"encrypted_{os.path.basename(image_path)}"
    with open(encrypted_image_path, 'wb') as file:
        file.write(encrypted_data)

    return encrypted_image_path

def decrypt_with_aes_ctr(encrypted_data, aes_key, file_extension):
    # Use Counter mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data

def decrypt_image(image_path, aes_key):
    with open(image_path, 'rb') as file:
        encrypted_data = file.read()

    # Get the original file extension from the image path
    _, file_extension = os.path.splitext(image_path)

    decrypted_data = decrypt_with_aes_ctr(encrypted_data, aes_key, file_extension)

    # Construct the output path for the decrypted image
    decrypted_image_path = f"decrypted_{os.path.basename(image_path)[:-len(file_extension)]}_decrypted{file_extension}"

    with open(decrypted_image_path, 'wb') as file:
        file.write(decrypted_data)

    print(f"Decrypted image saved at: {decrypted_image_path}")

def encrypt_image(image_path, rsa_public_key):
    try:
        # Generate AES key
        aes_key = generate_aes_key()

        # Encrypt the image using AES-CTR
        encrypted_image_path = encrypt_with_aes_ctr(image_path, aes_key)

        # Encrypt the AES key using RSA
        encrypted_aes_key = encrypt_aes_key(aes_key, rsa_public_key)
        aes_key_filename = f"encrypted_aes_key_{os.path.basename(image_path)}.txt"
        with open(aes_key_filename, 'w') as key_file:
            key_file.write(encrypted_aes_key)

        print(f"Encrypted image saved at: {encrypted_image_path}")
        print(f"AES key saved at: {aes_key_filename}")

        return encrypted_image_path, aes_key_filename
    except Exception as e:
        logging.error(f"Error during image encryption: {str(e)}")
        return None, None

def main():
    # Select an image
    image_path = select_image()

    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        sys.exit(1)

    print(f"Processing image at: {image_path.encode('utf-8')}")


    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Encrypt image and AES key
    encrypted_image_path, aes_key_filename = encrypt_image(image_path, public_key)

    if encrypted_image_path and aes_key_filename:
        print(f"Encryption successful!")

        # Decrypt AES key
        with open(aes_key_filename, 'r') as key_file:
            encrypted_aes_key = key_file.read()

        decrypted_aes_key = private_key.decrypt(
            base64.b64decode(encrypted_aes_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypt image
        decrypt_image(encrypted_image_path, decrypted_aes_key)
        print(f"Decryption successful!")
    else:
        print(f"Error during encryption. Check logs for details.")

if __name__ == "__main__":
    main()
