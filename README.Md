# Cloud-Based Security Framework for Web Applications

## Introduction

This repository introduces an advanced, cloud-based security framework designed specifically for web applications. The framework emphasizes robust data protection, efficient user management, and comprehensive system monitoring to enhance the security posture of digital platforms.

## Key Features

### 1. Data Protection
- **Cutting-Edge Encryption**: Utilizes advanced encryption techniques to safeguard user information and credentials.
- **Confidentiality Assurance**: Ensures sensitive data remains confidential and inaccessible to unauthorized parties.

### 2. User Management
- **Intuitive Interface**: Simplifies the management of roles and permissions through a user-friendly interface.
- **Optimized Access Control**: Streamlines access control processes, reducing administrative burden and enhancing security.

### 3. Real-Time Monitoring and Alerts
- **Transparency and Insights**: Provides detailed visibility into system operations for proactive monitoring.
- **Immediate Alerts**: Issues real-time alerts for unauthorized access attempts, enabling swift and decisive action.

### 4. Integration with Cloud Security Best Practices
- **Industry Standards Compliance**: Aligns with established cloud security best practices and protocols.
- **Regular Security Audits**: Conducts regular security audits to identify and address vulnerabilities proactively.

### 5. Regulatory Compliance
- **Adherence to Regulations**: Emphasizes compliance with data protection regulations and standards to ensure legal and ethical security measures.

## Benefits

- **Enhanced Security**: Robust encryption and real-time monitoring significantly reduce the risk of data breaches.
- **Operational Efficiency**: Streamlined user management processes free up administrative resources.
- **Proactive Threat Management**: Immediate alerts and regular audits help in early identification and mitigation of security threats.
- **Regulatory Confidence**: Compliance with industry standards and regulations instills confidence in the framework's reliability and effectiveness.

## Conclusion

This cloud-based security framework represents a comprehensive solution for web applications, focusing on data protection, efficient user management, and proactive security measures. By integrating best practices and ensuring compliance with regulations, it offers a robust and reliable security system for modern digital environments.


# RSA-AES Image Encryption Script

This script encrypts and decrypts image files using RSA and AES encryption. AES is used for encrypting the image data, while RSA encrypts the AES key. It utilizes the Tkinter library for file selection.

## Features

- **AES-256 Encryption**: Utilizes AES encryption in Counter (CTR) mode for image data encryption.
- **RSA Encryption**: Encrypts the AES key using RSA public key encryption.
- **GUI File Selection**: Uses Tkinter to provide a file dialog for selecting images.
- **File Handling**: Handles reading from and writing encrypted/decrypted data to files.

## Dependencies

- `cryptography`: Library for cryptographic recipes and primitives.
- `tkinter`: For GUI-based file selection.
- `Pillow (PIL)`: To handle image files.
- `os`, `sys`, `logging`, `base64`: Standard Python libraries for various utilities.

## Functions

- **generate_aes_key**: Generates a random 256-bit AES key.
- **select_image**: Opens a file dialog to select an image file.
- **encrypt_aes_key**: Encrypts the AES key using an RSA public key.
- **encrypt_with_aes_ctr**: Encrypts image data using AES in CTR mode.
- **decrypt_with_aes_ctr**: Decrypts data encrypted with AES in CTR mode.
- **decrypt_image**: Decrypts the encrypted image file.
- **encrypt_image**: Encrypts the image file and saves the encrypted AES key.

## Usage

To use the script, run the `main` function which will guide you through selecting an image, encrypting it, and then decrypting it.


## Notes

- Ensure the required libraries are installed using `pip install cryptography tkinter Pillow`.
- The script outputs the encrypted image and AES key in the current directory.


# PDF Encryption and Decryption Script Using RSA and AES

This script provides functionality to encrypt and decrypt PDF files using a combination of RSA and AES encryption. It uses the Tkinter library to provide a file dialog for selecting the PDF file.

## Features

- **RSA Key Pair Generation**: Generates RSA public and private keys.
- **File Encryption**: Encrypts PDF files using RSA and AES.
- **File Decryption**: Decrypts the encrypted PDF files.
- **GUI File Selection**: Uses Tkinter to select the PDF file.

## Dependencies

- `pycryptodome`: Library for cryptographic operations.
- `tkinter`: For GUI-based file selection.
- `os`: Standard Python library for various utilities.

## Functions

- **generate_rsa_key_pair**: Generates a 2048-bit RSA key pair.
- **save_key_to_file**: Saves a key to a specified file.
- **load_key_from_file**: Loads a key from a specified file.
- **encrypt_file_rsa**: Encrypts a file using RSA and AES.
- **decrypt_file_rsa**: Decrypts an encrypted file using RSA and AES.
- **choose_file**: Opens a file dialog to select a PDF file.
- **main**: Main function to orchestrate encryption and decryption process.

## Usage

To use the script, run the `main` function which will guide you through selecting a PDF file, encrypting it, and then decrypting it.


## Notes

- Ensure the required libraries are installed using `pip install pycryptodome tkinter`.
- The script outputs the encrypted file and keys in the current directory.
- The decrypted file will be saved with the suffix `_decrypted` in the current directory.


## RSA-AES Text Encryption Script

This script provides a solution for encrypting and decrypting text files using RSA and AES encryption. The AES key is used for encrypting the data, while the RSA public key encrypts the AES key itself.

### Features

- **AES-256 Encryption**: Uses AES encryption in Counter (CTR) mode for data encryption.
- **RSA Encryption**: Encrypts the AES key using RSA public key encryption.
- **Concurrent Processing**: Encrypts text file data in chunks concurrently to speed up the process.
- **File Handling**: Reads from and writes encrypted/decrypted data to files.

### Dependencies

- `cryptography`: Python library for cryptographic recipes and primitives.
- `concurrent.futures`: To handle concurrent execution of file chunk encryption.
- `os`, `sys`, `logging`, `base64`: Standard Python libraries for various utility functions.

### Functions

- **generate_aes_key**: Generates a random 256-bit AES key.
- **encrypt_aes_key**: Encrypts the AES key using an RSA public key.
- **encrypt_with_aes_ctr**: Encrypts data using AES in CTR mode.
- **decrypt_with_aes_ctr**: Decrypts data encrypted with AES in CTR mode.
- **encrypt_chunk**: Encrypts a data chunk with AES.
- **encrypt_text_file**: Encrypts a text file in chunks and returns encrypted data and the encrypted AES key.
- **main**: Main function to handle file processing, RSA key generation, and calling encryption/decryption functions.

### Usage

To use the script, call the `main` function with the path of the text file you want to encrypt:

```python
if __name__ == '__main__':
    file_path = 'path/to/your/textfile.txt'
    main(file_path)
```

### Notes

- Ensure the `cryptography` library is installed using `pip install cryptography`.
- Adjust the file paths as needed.
- The script outputs the encrypted and decrypted files in the user's Downloads directory.


#Cloud Security Framework  

This code defines a Flask web application that manages user registration, authentication, file uploads, and encryption. Below is a summary of the main functionalities and components of the application:

### Key Components

1. **Flask Application Configuration:**
   - Sets up the SQLite database.
   - Configures upload folders and secret keys.

2. **Database Model:**
   - Defines a `User` class with fields for username, password, last login, account creation timestamp, and login attempts.
   - Provides methods for updating the last login time and creating tables.

3. **User Registration and Authentication:**
   - `/register`: Handles user registration with password validation and hashing.
   - `/login`: Manages user login, validates credentials, and tracks login attempts.
   - `/logout`: Logs out the user and records the activity.
   - `/delete_account`: Allows users to delete their accounts, move logs, and deactivate the account.

4. **Admin Login:**
   - `/admin-login`: Provides a login interface for admins to view users.

5. **File Management:**
   - `/upload_text_file`, `/upload_image`, `/upload_document`: Handle file uploads, call respective scripts for encryption, and log activities.
   - `/viewfiles`: Displays a list of uploaded files.
   - `/delete_file/<filename>`: Deletes specified files and logs the activity.
   - `/download_file`: Allows users to download files and logs the activity.

6. **User Activity Logs:**
   - Logs various activities like login, file uploads, downloads, and deletions.
   - `/view_user_activity/<username>`: Displays user activity logs.

7. **Encryption:**
   - Integrates RSA and AES encryption for file handling using an external script `rsaaestxt.py`.

8. **User Management:**
   - `/view_users`: Displays a list of users and their details.
   - `/delete_user/<username>`: Deletes user accounts, moves logs, and removes user folders.

9. **Miscellaneous:**
   - Includes routes for home, cloud, and dashboard.
   - Uses Flask sessions to manage user login states.
   - Error handling for invalid file uploads and login attempts.

### Code Flow and Functionality
1. **App Initialization:**
   - Sets up the Flask app, configures the database, and initializes the secret key and upload folder.

2. **User Registration and Login:**
   - Registers new users, ensuring passwords meet security criteria.
   - Logs in users, checks hashed passwords, and manages login attempts.
   - Logs out users and records the activity.

3. **File Operations:**
   - Uploads and encrypts text files, images, and documents.
   - Views, downloads, and deletes files, logging each action.

4. **Admin Functions:**
   - Admin login to view and manage user accounts.
   - Deletes user accounts, moves logs, and updates user statuses.

5. **User Activity Tracking:**
   - Logs all significant user actions with timestamps.
   - Displays activity logs to admins.

### Security Measures
- Password hashing and validation.
- Session management for user authentication.
- Logging of user activities to maintain an audit trail.
- Handling of file operations securely with validation checks.

This application provides a comprehensive system for user management, secure file handling, and activity tracking, making it suitable for scenarios requiring strict user authentication and file security.
