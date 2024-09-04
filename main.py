from flask import Flask, render_template, send_file, request , jsonify
from flask_cors import CORS
from pvrecorder import PvRecorder
import wave
import struct
import sounddevice as sd
import soundcard as sc
import soundfile as sf
import pvrecorder

wav_file = None
wav_file1 = None
recording = False
soft_recording = False

app = Flask(__name__)
# needed for packs use
CORS(app)

# soft recorder 
soft_devices = PvRecorder.get_available_devices()
soft_recorder = PvRecorder(frame_length=512, device_index=0)

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
    global soft_recording, wav_file1

    #Todo warn macos that this will not work and use blackhole
    """ Windows & Linux ONLY """
    def callback(indata, outdata, frames, time, status):
        outdata[:] = indata

    # Replace 'virtual_audio_cable' with the actual name of virtual audio device
    with sd.InputStream(device='virtual_audio_cable', callback=callback):
        input()  # Wait for user input to stop recording

    """ failed attempt
    soft_recording = not soft_recording
    if soft_recording == False:
        wav_file1.close()
        wav_file1 = None
        soft_recorder.stop()
        soft_recorder.delete()

    if soft_recording == True:
        wav_file1 = wave.open('soft_recording.wav', 'wb')
        wav_file1.setnchannels(1) 
        wav_file1.setsampwidth(2)   
        wav_file1.setframerate(16000)  
        soft_recorder.start()

    while soft_recording:
        audio_frame = soft_recorder.read()
        audio_bytes = struct.pack('<' + ('h' * len(audio_frame)), *audio_frame)
        wav_file1.writeframes(audio_bytes)
    """

    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001) # change to ip and port for non-debug