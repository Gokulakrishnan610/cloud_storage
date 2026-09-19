# Cloud Storage

A lightweight Flask-based file and folder upload service for local/cloud-style storage. This project lets users upload individual files or an entire folder structure, browse uploaded items, and download any folder as a ZIP archive.

## Features
- Upload single files or whole folders
- Preserve folder structure during uploads
- View uploaded files from the browser
- Download an uploaded folder as a ZIP
- Simple local web UI with Flask templates
- Large upload handling (up to 1000MB per file)

## Project Structure
- `app.py` — Flask application and upload/download logic
- `templates/upload.html` — upload interface
- `uploads/` — local storage directory for uploaded content

## Requirements
- Python 3.10+
- Flask
- requests
- Werkzeug

## Setup

1. Create and activate a virtual environment:
   ```bash
   cd cloud_storage
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install flask requests
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open in browser:
   ```text
   http://localhost:5050
   ```

## Usage
- Select a file or folder from the upload page.
- Submit the form to store content under the local `uploads/` folder.
- Use the generated links to open or download uploaded files.
- Use the folder download button to export a directory as a ZIP archive.

## Notes
- This is designed as a local storage demo and stores files in the project directory.
- Since uploads are stored locally, they are excluded from Git by default via `.gitignore`.
