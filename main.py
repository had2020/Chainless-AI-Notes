from flask import Flask, render_template, send_file, request , jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import websockets
from flask_assets import Environment, Bundle
import sounddevice as sd
import numpy as np

app = Flask(__name__)
# needed for packs use
CORS(app)
socketio = SocketIO(app)
assets = Environment(app)

# Setting up uploads folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define bundles
js_bundle = Bundle('js/script1.js', 'js/script2.js', output='dist/bundle.js')
css_bundle = Bundle('css/style.css', output='dist/style.css')
assets.register('js_all', js_bundle)
assets.register('css_all', css_bundle)

# check the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Audio recording functionality
recording = False
audio_data = np.random.rand(10000)  # Example: Random noise

# Set up audio parameters
samplerate = 44100
channels = 1

# Create a continuous playback stream
stream = sd.OutputStream(samplerate=samplerate, channels=channels)
stream.start()

# Start the while loop
while recording == True:
    # Play the audio data
    stream.write(audio_data)

# Flask routes
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process():
    recording = True # TODO globalifty this
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001) # change to ip and port for non-debug