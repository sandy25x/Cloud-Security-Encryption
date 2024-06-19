from flask import Flask, abort, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
import pytz
import re
from werkzeug.utils import secure_filename
import os
import subprocess
from flask import send_from_directory
from flask import send_file
from rsaaestxt import main as rsa_aes_txt_main

from database import db
from utils import allowed_file  # Import the allowed_file function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\minij\\Downloads\\try\\instance\\user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'C:/Users/minij/Downloads/try/path/to/your/upload/folder'
db.init_app(app)


def some_function():
    from app import db


@app.route('/')
def home():
    if 'username' not in session or not session.get('username'):
        # Redirect to the login page if no user is logged in
        return redirect(url_for('login'))

    return f'Logged in as {session.get("username", "Unknown User")}'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    account_created_at = db.Column(db.DateTime, nullable=False)  # Add this line
    login_attempts = db.Column(db.Integer, default=0)

    def update_last_login(self):
        # Set the time zone to Indian Standard Time (IST)
        ist = pytz.timezone('Asia/Kolkata')
        self.last_login = datetime.now(ist)

    def check_and_update_activity(self):
        # Assume 'ist' is the Indian Standard Time (Asia/Kolkata)
        ist = pytz.timezone('Asia/Kolkata')


    def create_all_tables(self):
        with app.app_context():
            db.create_all()


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['adminUsername']
        password = request.form['adminPassword']

        # Check if the entered credentials are correct (replace with your own logic)
        if username == 'adminUsername' and password == 'adminPassword':
            # Set a session variable to indicate that the admin is logged in
            session['admin_logged_in'] = True
            # Redirect to the view_users page
            return redirect(url_for('view_users'))
        else:
            flash('Invalid admin username or password. Please try again.', 'error')

    return render_template('admin_login.html')

def is_username_existing(username):
    log_file_path = 'C:/Users/minij/Downloads/try/path/to/your/upload/folder/username_log.txt'
    with open(log_file_path, 'r') as log_file:
        existing_usernames = log_file.readlines()
        existing_usernames = [name.strip() for name in existing_usernames]
        if username in existing_usernames:
            return True
        else:
            return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match. Please try again.')

        # Check password requirements
        if (
            len(password) < 5 or
            len(re.findall(r'\d', password)) < 3 or
            not re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        ):
            return render_template('register.html', error='Password does not meet the requirements.')
        
        if is_username_existing(username):
            return render_template('register.html', error='Username already exists. Please choose a different one.')

        if not User.query.filter_by(username=username).first():
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(username=username, password=hashed_password, is_active=True)
            db.session.add(new_user)
            db.session.commit()

            # Create user folder and subfolders for images and documents
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
            os.makedirs(user_folder)

            # Create "encrypted files" folder inside the user's folder
            encrypted_files_folder = os.path.join(user_folder, "encrypted files")
            os.makedirs(encrypted_files_folder)

            # Create log file and store account creation timestamp
            log_file_path = os.path.join(user_folder, "activity_log.txt")
            with open(log_file_path, "a") as log_file:
                account_creation_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f"Account Created: {account_creation_timestamp}\n")

            log_username(username)
            flash('Account created successfully!', 'success')

            # Redirect to the login page with success parameter
            return redirect(url_for('login', success=True))
        else:
            return render_template('register.html', error='Username already exists. Please choose a different one.')

    return render_template('register.html')


# Update the view_files route to pass the list of files to the template
@app.route('/viewfiles')
def view_files():
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)

    # Check if the user folder exists
    if os.path.exists(user_folder):
        # List all files in the user folder excluding activity_log.txt
        files = [file for file in os.listdir(user_folder) if file != 'activity_log.txt']
    else:
        files = []

    return render_template('viewfiles.html', username=username, files=files)

@app.route('/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    file_path = os.path.join(user_folder, filename)

    print("Attempting to delete file:", file_path)  # Add this line for debugging

    # Check if the file exists
    if os.path.exists(file_path):
        print("File exists, attempting deletion...")  # Add this line for debugging
        record_deletion(username, filename)
        # Delete the file
        os.remove(file_path)
        
        # Remove the file from the list of files displayed in the table
        files = [file for file in os.listdir(user_folder) if file != 'activity_log.txt' and file != filename]
        
        print("File deleted successfully.")  # Add this line for debugging

        return jsonify({'success': True, 'files': files})
    else:
        print("File not found.")  # Add this line for debugging
        return jsonify({'success': False, 'message': 'File not found'})

MAX_LOGIN_ATTEMPTS = 3  # Define the maximum number of login attempts


def log_username(username):
    log_file_path = 'C:/Users/minij/Downloads/try/path/to/your/upload/folder/username_log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(username + '\n')

@app.route('/download_file')
def download_file():
    filename = request.args.get('filename')
    username = session.get('username')  # Assuming the username is stored in the session
    file_path = f'C:/Users/minij/Downloads/try/path/to/your/upload/folder/{username}/{filename}'
    record_download(username, filename)
    return send_file(file_path, as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        deleted_account_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'DELETED ACCOUNT')
        if any(username in filename for filename in os.listdir(deleted_account_folder)):
            flash('This account has been deactivated. Please contact the administrator.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                user.update_last_login()
                user.login_attempts = 0  # Reset login attempts on successful login
                db.session.commit()
                
                # Append login activity to the user's log file
                log_activity(username, "Login")
                
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                user.login_attempts += 1
                db.session.commit()

                if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
                    # Log the login error to the user's activity log and highlight it
                    log_activity(username, "Login Error", highlight=True)
                
                flash('Invalid username or password. Please try again.', 'error')
                return render_template('login.html')
        else:
                flash('This account has been deactivated. Please contact the administrator.', 'error')
                return render_template('login.html')
    else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')



# Code to view usernames and last login timestamps in the database
from alembic import op
import sqlalchemy as sa

# Replace this line with the actual version number of your migration
revision = 'xxxx'
down_revision = 'xxxx'  # Use the revision number of the previous migration, or None if it's the first migration
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('is_active', sa.Boolean(), default=True, nullable=False))


def downgrade():
    op.drop_column('user', 'is_active')


def format_timestamp(timestamp):
    if timestamp is None:
        return "Not logged in yet"

    if isinstance(timestamp, datetime):
        ist = pytz.timezone('Asia/Kolkata')
        return timestamp.astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')

    return "Invalid timestamp"


@app.route('/view_users')
def view_users():
    # Fetch user information from the database, excluding deleted accounts
    users = User.query.filter_by(is_active=True).all()

    # Update user activity before displaying
    for user in users:
        user.check_and_update_activity()

    # Assuming last_login is in the second position in the tuple (index 2)
    user_info = [
        (user.username, user.password, format_timestamp(user.last_login), user.is_active) for user in users
    ]

    # Render the view_users template with user information
    return render_template('view_users.html', user_info=user_info)



import shutil

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    # Find the user by username
    user = User.query.filter_by(username=username).first()

    if user:
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the deletion activity
        log_message = f"{timestamp}: Account Deleted\n"
        log_file_path = os.path.join(app.config['UPLOAD_FOLDER'], username, "activity_log.txt")
        with open(log_file_path, "a") as log_file:
            log_file.write(log_message)

        # Move the user's activity log file to the DELETED ACCOUNT folder
        source_log_path = log_file_path
        dest_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'DELETED ACCOUNT')
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        dest_log_path = os.path.join(dest_folder, f"{username}_activity_log.txt")
        shutil.move(source_log_path, dest_log_path)

        # Delete the user from the database

        db.session.delete(user)
        db.session.commit()

        # Delete the user's folder
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
            flash(f"User {username} and associated folder deleted successfully", 'success')
        else:
            flash(f"User {username} folder not found", 'error')
    else:
        flash(f"User {username} not found", 'error')

    # Redirect back to the view_users page
    return redirect(url_for('view_users'))

@app.route('/upload_text_file', methods=['POST'])
def upload_text_file():
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        # Log the "drop text file" activity
        log_activity(username, f"Text File Uploaded: {filename}")

        # Call the rsa_aes_txt_main function with the file_path as an argument
        message = rsa_aes_txt_main(file_path)

        return jsonify({'message': message})

    return jsonify({'error': 'Invalid file'})


@app.route('/cloud')
def cloud():
    return redirect(url_for('login'))

# Add route handler for the shield icon
@app.route('/shield')
def shield():
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session or not session.get('username'):
        # Redirect to the login page if not logged in
        return redirect(url_for('login'))

    # Get the username from the session
    username = session['username']

    # Render the user dashboard template with the username
    return render_template('dashboard.html', username=username)

@app.route('/get_uploaded_files')
def get_uploaded_files():
    # Get the username from the session
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)

    # Check if the user folder exists
    if os.path.exists(user_folder):
        # List all files in the user folder
        files = os.listdir(user_folder)
        return jsonify({'files': files})
    else:
        return jsonify({'files': []})


from datetime import datetime

@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Get the username from the session
    username = session.get('username')
    
    # Find the user by username
    user = User.query.filter_by(username=username).first()

    if user:
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user.is_active = False
        db.session.commit()
        # Log the deletion activity
        log_message = f"{timestamp}: Account Deleted\n"
        log_file_path = os.path.join(app.config['UPLOAD_FOLDER'], username, "activity_log.txt")
        with open(log_file_path, "a") as log_file:
            log_file.write(log_message)

        # Move the user's activity log file to the DELETED ACCOUNT folder
        source_log_path = log_file_path
        dest_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'DELETED ACCOUNT')
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        dest_log_path = os.path.join(dest_folder, f"{username}_activity_log.txt")
        shutil.move(source_log_path, dest_log_path)

        # Delete the user's folder
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
            flash(f"User {username} and associated folder deleted successfully", 'success')
        else:
            flash(f"User {username} folder not found", 'error')
            
        # Logout the user
        session.pop('username', None)
        return redirect(url_for('login'))
    else:
        flash(f"User {username} not found", 'error')

    # Redirect back to the dashboard
    return redirect(url_for('dashboard'))

import os

@app.route('/view_user_activity/<username>')
def view_user_activity(username):
    # Check if the activity log file exists in the user's folder
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    log_file_path = os.path.join(user_folder, "activity_log.txt")
    
    # Check if the activity log file exists in the DELETED ACCOUNT folder
    deleted_account_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'DELETED ACCOUNT')
    deleted_log_file_path = os.path.join(deleted_account_folder, f"{username}_activity_log.txt")
    
    # Determine the path of the activity log file
    if os.path.exists(log_file_path):
        activity_log_path = log_file_path
    elif os.path.exists(deleted_log_file_path):
        activity_log_path = deleted_log_file_path
    else:
        return abort(404)  # Return a 404 error if the activity log file doesn't exist
    
    # Read the content of the activity log file
    with open(activity_log_path, "r") as log_file:
        activity_log = log_file.read()
    
    # Render a template to display the activity log
    return render_template('view_user_activity.html', username=username, activity_log=activity_log)




@app.route('/uploads/<username>/<filename>')
def uploaded_file(username, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], username), filename)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        # Call the imgscrblr.py script with the file_path as an argument
        subprocess.run(['python', 'imgscrblr.py', file_path])

        # Append image upload activity to the user's log file
        log_activity(username, f"Image Uploaded")

        # Construct the message indicating where the image is uploaded
        message = f'Image uploaded and encrypted successfully.'

        return jsonify({'message': message})

    return jsonify({'error': 'Invalid file'})

# Route to handle document upload
@app.route('/upload_document', methods=['POST'])
def upload_document():
    username = session.get('username')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        # Call the docscrblr.py script with the file_path as an argument
        subprocess.run(['python', 'docscrblr.py', file_path])

        # Append document upload activity to the user's log file
        log_activity(username, f"Document Uploaded")

        return jsonify({'message': 'Document uploaded and encrypted successfully'})

    return jsonify({'error': 'Invalid file'})



@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        # Append logout activity to the user's log file
        log_activity(username, "Logout")
    session.pop('username', None)
    return redirect(url_for('login'))


def log_activity(username, activity, highlight=False):
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Create log message with username, activity, and timestamp
    log_message = f"{timestamp}: {username} - {activity}\n"
    if highlight:
        log_message = f"<span style='color:red'>{log_message}</span>"
    # Define log file path
    log_file_path = os.path.join(app.config['UPLOAD_FOLDER'], username, "activity_log.txt")
    # Append log message to the log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)


def record_deletion(username, filename):
    log_activity(username, f"Deleted file '{filename}'")

def record_download(username, filename):
    log_activity(username, f"Downloaded file '{filename}'")

if __name__ == '__main__':
    app.run(debug=True)
