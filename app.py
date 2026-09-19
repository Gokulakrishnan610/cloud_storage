from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import socket
import requests
import shutil
import zipfile
from io import BytesIO
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set()  # Empty set means all file types are allowed
MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000MB (1GB) max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_ip():
    try:
        # Get public IP using a reliable service
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
    except:
        # Fallback to local IP if public IP cannot be retrieved
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    return 'localhost'

def allowed_file(filename):
    return True

def get_file_structure():
    structure = []
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        if root == UPLOAD_FOLDER:
            # Add files in root directory
            for file in files:
                structure.append({'type': 'file', 'name': file})
            # Add folders
            for dir in dirs:
                folder_files = os.listdir(os.path.join(UPLOAD_FOLDER, dir))
                structure.append({
                    'type': 'folder',
                    'name': dir,
                    'files': folder_files
                })
    return structure

@app.route('/')
def upload_form():
    ip_address = get_ip()
    port = 5000
    file_structure = get_file_structure()
    return render_template('upload.html', 
                         file_structure=file_structure, 
                         ip_address=ip_address, 
                         port=port)

@app.route('/upload-folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        return "No folder selected", 400

    files = request.files.getlist('files[]')
    
    # Check number of files
    if len(files) > 500000:
        return "Too many files. Maximum limit is 500,000 files.", 413
    
    for file in files:
        if file.filename:
            # Get the relative path within the uploaded folder
            relative_path = file.filename
            
            # Create the full path including any subdirectories
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path)
            
            # Create necessary subdirectories
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            if allowed_file(file.filename):
                try:
                    file.save(full_path)
                except Exception as e:
                    return f"Error uploading {file.filename}: {str(e)}", 500

    return redirect(url_for('upload_form'))

@app.route('/uploads/<path:folder>/<path:filename>')
def uploaded_file(folder, filename):
    try:
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)
    except Exception as e:
        return str(e), 404

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/download-folder/<folder_name>')
def download_folder(folder_name):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    if not os.path.exists(folder_path):
        return "Folder not found", 404
        
    # Create memory file
    memory_file = io.BytesIO()
    
    # Create the zip file in memory
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arc_name)
    
    # Reset file pointer
    memory_file.seek(0)
    
    # Return the zip file with proper mimetype
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{folder_name}.zip"
    )

if __name__ == '__main__':
    # Run the app on all network interfaces
    app.run(host='0.0.0.0', port=5050, debug=True)
