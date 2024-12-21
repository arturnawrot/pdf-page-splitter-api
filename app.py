from flask import Flask, request, jsonify, send_from_directory
from PyPDF2 import PdfReader, PdfWriter
from urllib.parse import urlparse
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.routing import BaseConverter
import os
import time
import uuid
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

scheduler = BackgroundScheduler()
scheduler.start()

def delete_files():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        if is_file_old(filename, now):
            os.remove(os.path.join(UPLOAD_FOLDER, filename))

def is_file_old(filename, now):
    return os.stat(os.path.join(UPLOAD_FOLDER, filename)).st_mtime < now - 48 * 60 * 60

scheduler.add_job(func=delete_files, trigger="interval", hours=1)

@app.route('/<regex("fixtures|uploaded_files"):folder>/<path:filename>')
def serve_files(folder, filename):
    return send_from_directory(folder, filename)

@app.route('/split-pdf', methods=['POST'])
def split_pdf():
    url = request.json.get('url')

    if not url:
        return "No URL provided", 400
    
    # Please note that even if a URL does not end with .pdf, it can still link to a PDF file.
    # if not is_pdf(url):
    #     return "Given URL does not end with .pdf format", 400

    content, status = fetch_pdf(url)
    if status != 200:
        return content, status

    return process_pdf(content, url)

def is_pdf(filepath):
    return filepath.lower().endswith('.pdf')

def fetch_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content, 200
    except requests.exceptions.RequestException as e:
        error_message = f"Error accessing URL: {str(e)}"
        status_code = 404 if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404 else 400
        return error_message, status_code

def process_pdf(content, url):
    filename = urlparse(url).path.split('/')[-1]
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        with open(original_path, 'wb') as f:
            f.write(content)

        reader = PdfReader(original_path)
        output_urls = [generate_pdf(page) for page in reader.pages]
        return jsonify(output_urls), 200
    except Exception as e:
        return f"Failed to process PDF: {str(e)}", 500

def generate_pdf(page):
    writer = PdfWriter()
    writer.add_page(page)

    random_uuid = uuid.uuid4()

    output_filename = f"{random_uuid}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    return request.host_url + UPLOAD_FOLDER + '/' + output_filename

if __name__ == '__main__':
    app.run(debug=True)