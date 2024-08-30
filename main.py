from flask import Flask, render_template, send_file, request , jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import websockets
from flask_assets import Environment, Bundle

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

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_save_path)
        
        pngtopdf(image_save_path)

        #return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
        os.remove(image_save_path)
        return send_file('pdf-with-image.pdf', as_attachment=True, mimetype='application/pdf')
    else:
        return jsonify({'error': 'File type not allowed'}), 400
""" Todo replace pyaudio https://python-sounddevice.readthedocs.io/en/0.4.7/usage.html
@socketio.on('toggle_mic')
def handle_toggle_mic(data):
    global stream
    if stream is None:
        # starting up audio stream
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        emit('mic_status', {'status': 'started'})
        # sending audio data in a separate thread
        def send_audio_data():
            while stream.is_active():
                data = stream.read(CHUNK)
                emit('audio_data', data)
        socketio.start_background_task(send_audio_data)
    else:
        # stopping audio stream
        stream.stop_stream()
        stream.close()
        stream = None
        emit('mic_status', {'status': 'stopped'})
"""

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001) # change to ip and port for non-debug