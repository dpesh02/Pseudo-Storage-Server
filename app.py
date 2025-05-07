from flask import Flask, jsonify, Response
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from GitHub Pages frontend

load_dotenv()
API_KEY = os.getenv('GOOGLE_DRIVE_API_KEY')
print(f"[INIT] Loaded API Key: {'Set' if API_KEY else 'Missing!'}")

# Album to Google Drive folder ID mapping
folder_ids = {
    'album1': '1aIagh9HNCb6csvbWsE5k13F04eMpKbyw'
}
print(f"[INIT] Defined albums: {list(folder_ids.keys())}")

# Health check
@app.route('/')
def index():
    print("[ROUTE] / (index) accessed")
    return jsonify({"message": "Drive Gallery API is online."})

# List images in a Google Drive folder (album)
@app.route('/api/files/<album>')
def list_files(album):
    print(f"\n[ROUTE] /api/files/{album} called")

    folder_id = folder_ids.get(album)
    if not folder_id:
        print("[ERROR] Album not found in mapping")
        return jsonify({"error": "Album not found"}), 404

    print(f"[INFO] Using folder ID: {folder_id}")

    all_files = []
    nextPageToken = ''
    page_count = 0

    while True:
        page_count += 1
        print(f"[INFO] Fetching page {page_count}...")

        url = (
            f"https://www.googleapis.com/drive/v3/files"
            f"?q='{folder_id}'+in+parents+and+mimeType+contains+'image/'"
            f"&orderBy=name"
            f"&fields=files(id,name,mimeType,thumbnailLink),nextPageToken"
            f"&pageSize=100"
            f"&pageToken={nextPageToken}"
            f"&key={API_KEY}"
        )

        print(f"[DEBUG] URL: {url}")

        try:
            response = requests.get(url)
            print(f"[HTTP] Response status: {response.status_code}")
            data = response.json()

            if 'files' in data:
                print(f"[INFO] {len(data['files'])} file(s) found on page {page_count}")
                for file in data['files']:
                    all_files.append({
                        'id': file['id'],
                        'name': file['name'],
                        'thumbnail': file.get('thumbnailLink'),
                        'full_url': f"/api/image/{file['id']}"
                    })
            else:
                print("[WARN] No 'files' key in response")

            nextPageToken = data.get('nextPageToken')
            if not nextPageToken:
                print("[INFO] No more pages")
                break

        except Exception as e:
            print(f"[ERROR] Exception occurred: {str(e)}")
            return jsonify({"error": str(e)}), 500

    print(f"[DONE] Total files retrieved: {len(all_files)}")
    return jsonify(all_files)

# Image proxy: stream actual image data
@app.route('/api/image/<file_id>')
def proxy_image(file_id):
    google_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"
    try:
        response = requests.get(google_url, stream=True)
        return Response(
            response.iter_content(chunk_size=4096),
            content_type=response.headers.get('Content-Type', 'application/octet-stream'),
            status=response.status_code
        )
    except Exception as e:
        print(f"[ERROR] Image proxy failed: {e}")
        return jsonify({"error": "Failed to fetch image"}), 500

# Run the app
if __name__ == '__main__':
    print("[START] Starting Flask app...")
    app.run(debug=True)
