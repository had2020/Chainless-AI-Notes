from flask import Flask, render_template, send_file, request , jsonify
from flask_cors import CORS
from pvrecorder import PvRecorder
import wave
import struct
import sounddevice as sd
import soundcard as sc
import soundfile as sf

wav_file = None
recording = False
soft_recording = False

app = Flask(__name__)
# needed for packs use
CORS(app)

devices = PvRecorder.get_available_devices()
print("Available audio devices:")
for i, device in enumerate(devices):
    print(f"{i}: {device}")

devices = PvRecorder.get_available_devices()
recorder = PvRecorder(frame_length=512, device_index=0)

# frame processing
while recorder.is_recording:
    frame = recorder.read()

# Flask routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/record', methods=['POST', 'GET'])
def process():
    global recording, wav_file
    recording = not recording 
    if recording == False:
        wav_file.close()
        wav_file = None
        recorder.stop()
        recorder.delete()
    if recording == True:
        # Open a WAV file for writing
        wav_file = wave.open('recording.wav', 'wb')
        wav_file.setnchannels(1)  # Mono channel
        wav_file.setsampwidth(2)   # 16-bit audio
        wav_file.setframerate(16000)  # Sample rate of 16kHz 

        recorder.start()

    while recording:
            audio_frame = recorder.read()
            # convert list of integers (audio_frame) to bytes
            audio_bytes = struct.pack('<' + ('h' * len(audio_frame)), *audio_frame)
            wav_file.writeframes(audio_bytes)

    return render_template('index.html')

@app.route('/record_software', methods=['POST', 'GET'])
def record_software():
    global soft_recording, wav_file

    output_file_name = "soft_out.wav"
    samplerrate = 48000
    duration = 5
    
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerrate) as mic:
        data = mic.record(numframes=samplerrate*duration)
        sf.write(file=output_file_name, data=data[:, 0], samplerate=samplerrate)
    
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001) # change to ip and port for non-debug