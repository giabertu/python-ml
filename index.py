from flask import Flask, request, jsonify
# Import your AudioUtill class here
from audioUtil import AudioUtil
from supabaseClient import supabase

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Audio Processing API'

@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Get the file name from the request body
    data = request.json
    file_name = data.get('file_name')
    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400
    
    # Download the file from Supabase storage
    try:
        file_path = f'audio_files/{file_name}'
        downloaded_file = supabase.storage.from_('audio_files').download(file_path)
        if downloaded_file.status_code == 200:
            # Assuming you want to process the file here with your AudioUtil class
            # For example: result = AudioUtil.process(downloaded_file)
            return jsonify({'message': 'File processed successfully', 'data': 'Mock data'})
        else:
            return jsonify({'error': 'Failed to download file from Supabase'}), downloaded_file.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
