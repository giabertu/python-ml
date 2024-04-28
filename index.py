from flask import Flask, request,  jsonify
from audioUtil import AudioUtil
from supabaseClient import supabase
from flask_cors import CORS
from inference import get_emotion
import subprocess
from openAi import aiClient
from emotionClasses import emotions
import os

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Audio Processing API'


@app.route('/process_audio', methods=['POST'])
def process_audio():
    data = request.json
    file_path = data.get('filePath')
    print("Here is the filename:", file_path)
    if not file_path:
        return jsonify({'error': 'No file name provided'}), 400
    
    # Download the file from Supabase storage
    try:
        file_to_open = './files/' + file_path.split('/')[1]  # Define the file to open
        output_file = "./files/" + file_path.split('/')[1].split('.')[0] + '.wav'

        with open(file_to_open, 'wb+') as f:
            res = supabase.storage.from_('audio-files').download(file_path)
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

        emotion = get_emotion(output_file)
        print("Emotion:", emotion)

        audio_file= open(output_file, "rb")
        transcription = aiClient.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        print(transcription)
        print(transcription.text)
        audio_text = transcription.text

        # Process text and get the emotion

        completion = aiClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You have two tasks. First, you need to analyse the following text and provide your estimated emotion. Secondly, you need to give a hybrid emotion prediction, considering your predicted emotion, and the emotion prediction I provide you. You should keep in mind that the emotion prdiction you are provided is wrong 40 per cent of the time. So give more weight to your prediction. You need to reply in the following format: {\"textEmotion\": \"Natural\", \"hybridEmotion\": \"Happy\"}. The list of available emotions are: Angry, Disgusted, Fearful, Neutral, Happy, Sad. It is mandatory that you reply with the above format in any circumstance, even if there is no text to analyse (in which case you should assume neutral)" },
            {"role": "user", "content": "Here is the predicted emotion: " + emotions[emotion] + ". Here is the text audio to analyse: " + audio_text},
        ]
        )

        print(completion)
        print(completion.choices[0].message)
    
        llmRes = completion.choices[0].message

        return jsonify({
            'message': 'Audio processed successfully', 
            'modelPredictedEmotion': emotions[emotion], 
            'transcript': audio_text,
            'filePath':file_path,
            'llmRes': llmRes.content
            })
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'message': str(e)}), 500
    finally:
        if os.path.exists(file_to_open):
            os.remove(file_to_open)
        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == '__main__':
    app.run(debug=False, port=5000)
