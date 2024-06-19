import os
from cryptography.hazmat.primitives.asymmetric import rsa
import logging
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import sys
import concurrent.futures

def generate_aes_key():
    return os.urandom(32)  # 256 bits for AES-256

def encrypt_aes_key(aes_key, rsa_public_key):
    encrypted_key = rsa_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_key).decode('utf-8')

def encrypt_with_aes_ctr(data, aes_key):
    # Use Counter mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'\0' * 16), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    return encrypted_data

def decrypt_with_aes_ctr(encrypted_data, aes_key):
    # Use Counter mode
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(b'\0' * 16), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data

def encrypt_chunk(chunk, aes_key):
    return encrypt_with_aes_ctr(chunk, aes_key)

def encrypt_text_file(text_file_path, aes_key, rsa_public_key, chunk_size=65536):
    try:
        # Encrypt the text file using AES-CTR
        with open(text_file_path, 'rb') as file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                encrypted_chunks = list(executor.map(encrypt_chunk, iter(lambda: file.read(chunk_size), b''), [aes_key] * 100))
            
        encrypted_data = b''.join(encrypted_chunks)
        encrypted_aes_key = encrypt_aes_key(aes_key, rsa_public_key)
        
        print("Encrypted Text:")
        print(encrypted_data)


        return encrypted_data, encrypted_aes_key
    except Exception as e:
        logging.error(f"Error during text file encryption: {str(e)}")
        return None, None

def main(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    print(f"Processing text file at: {file_path}")

    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Generate AES key
    aes_key = generate_aes_key()

    # Encrypt text file
    encrypted_data, encrypted_aes_key = encrypt_text_file(file_path, aes_key, public_key)

    if encrypted_data and encrypted_aes_key:
        # Get the Downloads directory path
        downloads_dir = os.path.expanduser("~/Downloads")

        # Construct output file paths for encrypted and decrypted text files in the Downloads directory
        encrypted_text_file_path = os.path.join(downloads_dir, f"encrypted_{os.path.basename(file_path)}")
        decrypted_text_file_path = os.path.join(downloads_dir, f"decrypted_{os.path.basename(file_path)}")

        # Write encrypted data to the encrypted text file
        with open(encrypted_text_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print(f"Encrypted text saved at: {encrypted_text_file_path}")

        # Decrypt text file
        decrypted_data = decrypt_with_aes_ctr(encrypted_data, aes_key)

        # Write decrypted data to the decrypted text file
        with open(decrypted_text_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"Decrypted text saved at: {decrypted_text_file_path}")
    else:
        print(f"Error during encryption.")
