from audioUtil import AudioUtil
import torch
from audioClassifier import myModel, device

SAMPLE_RATE = 16000
CHANNELS = 2

class_id_mapping = {'A': 0, 'D': 1, 'F': 2, 'H': 3, 'N': 4, 'S': 5}


def process_audio_file(file_path, sample_rate, channels):
    aud = AudioUtil.open(file_path)
    reaud = AudioUtil.resample(aud, sample_rate)
    rechan = AudioUtil.rechannel(reaud, channels)
    sgram = AudioUtil.spectro_gram(rechan, n_mels=64, n_fft=1024, hop_len=None)
    aug_sgram = AudioUtil.spectro_augment(sgram, max_mask_pct=0.01, n_freq_masks=2, n_time_masks=2)

    # Normalize the spectrogram
    inputs = aug_sgram.unsqueeze(0)  
    inputs_m, inputs_s = inputs.mean(), inputs.std()
    normalized_inputs = (inputs - inputs_m) / inputs_s

    return normalized_inputs





#Function for single file inference
def single_file_inference(model, processed_input):
    model.eval()

    processed_input = processed_input.to(device)

    with torch.no_grad():
        print("proc input: ", processed_input)
        outputs = model(processed_input)
        print(outputs)

        _, prediction = torch.max(outputs, 1)

    return prediction.item()


def get_emotion(file_path):
    # Process the audio file
    processed_input = process_audio_file(file_path, SAMPLE_RATE, CHANNELS)

    # Predict the emotional state
    predicted_class_id = single_file_inference(myModel, processed_input)

    # Create a reverse mapping
    id_to_emotion = {v: k for k, v in class_id_mapping.items()}

    print(f'Predicted Class ID: {predicted_class_id}')

    predicted_emotion = id_to_emotion[predicted_class_id]

    print(f'Predicted Emotion: {predicted_emotion}')

    return predicted_emotion


