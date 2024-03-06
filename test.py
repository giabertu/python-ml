import torchaudio
from supabaseClient import supabase
import librosa


# with open('./files/super_happy.wav', 'wb+') as f:
#         res = supabase.storage.from_('audio-files').download('super_happy.wav')
#         print(res)
#         f.write(res)

# print(torchaudio.utils.sox_utils.list_read_formats())
# print(torchaudio.utils.ffmpeg_utils.get_audio_decoders())
# sig, sr = torchaudio.load('./files/file.wav')

print(torchaudio.load('./files/output.wav'))

# print(sig, sr)

#### This works so it implies that there is a problem with me createing the audio file on the client side