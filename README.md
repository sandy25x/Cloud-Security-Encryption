INTRODUCTION

The proposed concept introduces an advanced, cloud-based security framework 
meticulously designed for web applications, representing a significant evolution in the 
realm of digital security. At its core lies a profound commitment to safeguarding the 
integrity and privacy of user data, recognizing it as a paramount concern in today's 
interconnected digital landscape. Leveraging cutting-edge encryption techniques, the 
framework establishes a robust shield around user information and credentials, ensuring 
that sensitive data remains confidential and inaccessible to unauthorized parties. 

In addition to its focus on data protection, the framework addresses the complexities of user 
management with a keen eye towards optimization and efficiency. Through an intuitive and 
user-friendly interface, administrators are empowered to manage roles and permissions with 
ease, streamlining the process of access control and bolstering overall security posture. This 
streamlined approach not only enhances security but also reduces administrative burden, 
allowing organizations to allocate resources more effectively and focus on strategic 
objectives. Furthermore, the framework sets itself apart with its commitment to 
transparency and real-time insights into user activity. By providing administrators with 
detailed visibility into system operations, it enables proactive monitoring and response to 
potential security threats. Immediate alerts for unauthorized access attempts serve as an 
early warning system, empowering administrators to take swift and decisive action to 
mitigate risks and protect sensitive data from compromise. 

The integration of established cloud security best practices further strengthens the framework's resilience, ensuring that it remains in alignment with industry standards and 
best-in-class security protocols. Regular security audits serve as a proactive measure to 
identify and address vulnerabilities before they can be exploited, enhancing the overall 
robustness of the system and instilling confidence in its reliability and effectiveness. 
Moreover, the framework places a strong emphasis on regulatory compliance, recognizing the importance of adhering to data protection regulations and standards.


Image Encryption and Decryption Tool

  -This Python script provides a GUI-based application to encrypt and decrypt image files using a combination of RSA and AES cryptography. The script leverages the cryptography library for encryption tasks and tkinter for the file selection GUI.
  
  Features:
  AES Key Generation
  
  -Generates a random 256-bit AES key for encrypting image data.
  
  Image Selection
  
  -Uses tkinter to open a file dialog for selecting an image file.
  
  RSA Key Generation
  
  -Generates a 2048-bit RSA key pair for encrypting the AES key.
  
  Encryption
  
  -Encrypts the selected image using AES in CTR mode.
  -Encrypts the AES key using the RSA public key.
  -Saves the encrypted image and the encrypted AES key to files.
  
  Decryption
  
  -Decrypts the AES key using the RSA private key.
  -Decrypts the encrypted image using the decrypted AES key.
  -Saves the decrypted image to a file.
  
  Detailed Breakdown
  
  Functions:
  
  -generate_aes_key(): Generates a 256-bit AES key.
  -select_image(): Opens a file dialog to select an image file.
  -encrypt_aes_key(aes_key, rsa_public_key): Encrypts the AES key using the RSA public key and returns the base64-encoded result.
  -encrypt_with_aes_ctr(image_path, aes_key): Encrypts the image using AES in CTR mode and saves the encrypted image.
  -decrypt_with_aes_ctr(encrypted_data, aes_key, file_extension): Decrypts data using AES in CTR mode.
  -decrypt_image(image_path, aes_key): Decrypts an encrypted image file.
  -encrypt_image(image_path, rsa_public_key): Coordinates the encryption of the image and AES key.
  
  Main Workflow:
  
  -The user selects an image file via a file dialog.
  -The script generates an RSA key pair.
  -The selected image is encrypted with an AES key, which is then encrypted with the RSA public key.
  -The encrypted image and AES key are saved to files.
  -The AES key is decrypted using the RSA private key.
  -The image is decrypted using the decrypted AES key and saved to a file.
  
  Usage
  
  -To use this script, run it in a Python environment. The Tkinter GUI will prompt you to select an image file. The script will handle encryption and decryption, saving the resulting files in the working directory.
  
  Dependencies
  
  -tkinter: For the file selection GUI.
  -cryptography: For cryptographic operations (install with pip install cryptography).
  -Pillow: For image handling (install with pip install pillow).


PDF Encryption and Decryption Tool

  -This script provides a simple GUI-based tool for encrypting and decrypting PDF files using RSA and AES encryption. Here's a summary of its functionality:
  
  Features:
  
  RSA Key Pair Generation
  
  -Generates a 2048-bit RSA key pair (private and public keys).
  -Saves the keys to files (private.pem and public.pem).
  
  File Encryption
  
  -Uses the public RSA key to encrypt a randomly generated AES session key.
  -Encrypts a selected PDF file using the AES session key.
  -Saves the encrypted session key, nonce, tag, and ciphertext to an output file (encrypted_document.bin).
  
  File Decryption
  
  -Uses the private RSA key to decrypt the AES session key.
  -Decrypts the encrypted file using the AES session key.
  -Saves the decrypted content to an output PDF file (decrypted_document.pdf).
  
  File Selection GUI
  
  -Uses Tkinter to provide a file selection dialog for choosing the PDF file to encrypt.
  
  Detailed Breakdown
  
  Functions:
  
  -generate_rsa_key_pair(): Generates and returns an RSA key pair.
  -save_key_to_file(key, filename): Saves a given key to a file.
  -load_key_from_file(filename): Loads a key from a file.
  -encrypt_file_rsa(input_file, output_file, public_key_file): Encrypts a file using RSA and AES.
  -decrypt_file_rsa(input_file, output_file, private_key_file): Decrypts a file using RSA and AES.
  -choose_file(initialdir=None): Opens a file dialog to select a PDF file.
  
  Main Workflow:
  
  -The user selects a PDF file through a file dialog.
  -An RSA key pair is generated and saved to files.
  -The selected PDF file is encrypted and saved as encrypted_document.bin.
  -The encrypted file is then decrypted and saved as decrypted_document.pdf.
  
  Usage
  -To use this script, run it in a Python environment. The Tkinter GUI will prompt you to select a PDF file, and the script will handle encryption and decryption, saving the resulting files in the working directory.
  
  Dependencies
  
  -tkinter: For the file selection GUI.
  -pycryptodome: For cryptographic operations (install with pip install pycryptodome).


Text File Encryption and Decryption Tool

  -This Python script provides a tool for encrypting and decrypting text files using a combination of RSA and AES cryptography. It utilizes the cryptography library for cryptographic operations and supports concurrent processing to handle large files efficiently.
  
  Features:
  
  AES Key Generation
  
  -Generates a 256-bit AES key for encrypting file data.
  
  RSA Key Generation
  
  -Generates a 2048-bit RSA key pair for encrypting the AES key.
  
  File Encryption
  
  -Splits the input text file into chunks.
  -Encrypts each chunk using AES in CTR mode concurrently.
  -Encrypts the AES key using the RSA public key.
  -Combines encrypted chunks and prints the encrypted data.
  
  File Decryption
  
  -Decrypts the AES key using the RSA private key.
  -Decrypts the combined encrypted data using the decrypted AES key.
  
  Detailed Breakdown
  
  Functions:
  
  -generate_aes_key(): Generates a 256-bit AES key.
  -encrypt_aes_key(aes_key, rsa_public_key): Encrypts the AES key using the RSA public key and returns the base64-encoded result.
  -encrypt_with_aes_ctr(data, aes_key): Encrypts data using AES in CTR mode.
  -decrypt_with_aes_ctr(encrypted_data, aes_key): Decrypts data using AES in CTR mode.
  -encrypt_chunk(chunk, aes_key): Encrypts a chunk of data using AES in CTR mode.
  -encrypt_text_file(text_file_path, aes_key, rsa_public_key, chunk_size=65536): Encrypts a text file by splitting it into chunks, encrypting each chunk, and encrypting the AES key.
  
  Main Workflow:
  
  -The script checks if the specified text file exists.
  -Generates an RSA key pair.
  -Generates an AES key.
  -Encrypts the text file using AES and the AES key using RSA.
  -Saves the encrypted data and encrypted AES key to files.
  -Decrypts the AES key and the encrypted text file.
  -Saves the decrypted data to a file.
  
  Usage
  
  -To use this script, run it in a Python environment, specifying the path to the text file you want to encrypt. The script will handle encryption and decryption, saving the resulting files in the Downloads directory.
  
  Dependencies
  
  -cryptography: For cryptographic operations (install with pip install cryptography).
  -concurrent.futures: For concurrent processing.


Cloud Security Framework  

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
