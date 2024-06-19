from tkinter import Tk, filedialog
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def load_key_from_file(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

def encrypt_file_rsa(input_file, output_file, public_key_file):
    data = open(input_file, 'rb').read()
    recipient_key = RSA.import_key(load_key_from_file(public_key_file))
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    with open(output_file, 'wb') as f:
        [f.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

def decrypt_file_rsa(input_file, output_file, private_key_file):
    private_key = RSA.import_key(load_key_from_file(private_key_file))
    with open(input_file, 'rb') as f:
        enc_session_key, nonce, tag, ciphertext = [f.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    with open(output_file, 'wb') as f:
        f.write(data)

def choose_file(initialdir=None):
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        initialdir=initialdir,
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    root.destroy()  # Destroy the Tkinter instance
    return file_path

def main():
    # Choose PDF file for encryption
    pdf_file_path = choose_file()
    if not pdf_file_path:
        print("No file selected. Exiting.")
        exit()

    # Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair()
    save_key_to_file(private_key, "private.pem")
    save_key_to_file(public_key, "public.pem")

    # Encrypt chosen PDF file
    encrypt_file_rsa(pdf_file_path, "encrypted_document.bin", "public.pem")

    # Decrypt encrypted file
    decrypt_file_rsa("encrypted_document.bin", "decrypted_document.pdf", "private.pem")

if __name__ == "__main__":
    main()
