from flask import Flask, render_template, send_file, request , jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_assets import Environment, Bundle
from pvrecorder import PvRecorder

app = Flask(__name__)
# needed for packs use
CORS(app)

devices = PvRecorder.get_available_devices()
recorder = PvRecorder(frame_length=512, device_index=0)

while recorder.is_recording:
    frame = recorder.read()
    # process audio frame

# Flask routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process():
    global recording
    print(recording)
    recording = not recording 
    if recording == False:
        print("Recording stopped")
        recorder.stop()
    while recording == True:
        recorder.start()
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001) # change to ip and port for non-debug