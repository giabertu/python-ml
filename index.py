from flask import Flask, request,  jsonify
from audioUtil import AudioUtil
from supabaseClient import supabase
from flask_cors import CORS
from inference import get_emotion
import subprocess

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Audio Processing API'


@app.route('/process_audio', methods=['POST'])
# def process_audio():
#     # return jsonify({'message': 'File processed successfully', 'data': 'Mock data'})
#     data = request.json
#     file_name = data.get('filePath')
#     print("here is the filename " , file_name)
#     if not file_name:
#         return jsonify({'error': 'No file name provided'}), 400
    
#     # Download the file from Supabase storage
#     try:
#       file_to_open = './files/file.webm'
#       with open(file_to_open, 'wb+') as f:
#         res = supabase.storage.from_('audio-files').download(file_name)
#         print(res)
#         f.write(res)

#         # Get the emotional state
#         # test_file_path = './test_files/super_happy.wav'
#         # emotion = get_emotion(test_file_path)
#         emotion = get_emotion(file_to_open)
#         print("emotion: ", emotion)
#         return jsonify({'message': 'File processed successfully', 'data': emotion})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

def process_audio():
    data = request.json
    file_name = data.get('filePath')
    print("Here is the filename:", file_name)
    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400
    
    # Download the file from Supabase storage
    try:
        file_to_open = './files/file.webm'
        output_file = './files/file.wav'  # Define the output WAV file path

        with open(file_to_open, 'wb+') as f:
            # Assuming 'supabase' is your initialized Supabase client
            res = supabase.storage.from_('audio-files').download(file_name)
            f.write(res)

        # Convert the downloaded file to PCM S16 LE format using ffmpeg
        command = [
            'ffmpeg',
            '-i', file_to_open,  # Input file
            '-acodec', 'pcm_s16le',  # Codec
            '-ar', '44100',  # Sample rate
            '-ac', '1',  # Audio channels
            output_file  # Output file
        ]
        subprocess.run(command, check=True)

        # Assuming get_emotion is a function defined elsewhere that processes the WAV file
        emotion = get_emotion(output_file)
        print("Emotion:", emotion)

        return jsonify({'message': 'File processed successfully', 'data': emotion})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5000)
