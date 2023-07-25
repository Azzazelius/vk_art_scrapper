from flask import Flask, send_from_directory
from scrapper import run_scrapper
import os

app = Flask(__name__)

@app.route('/download_images', methods=['POST'])
def download_images_handler():
    return run_scrapper()

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, ''), 'index.html')

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

