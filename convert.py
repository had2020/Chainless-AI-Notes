import speech_recognition as sr
from os import path

def convert_to_text():
    print("Converting audio to text...")
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "recording.wav")

    # use audio file as audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read entire file

    # recognize speech with sphinx
    try:
        converted_text = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + converted_text)
        write_to_file(converted_text)
        return converted_text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        write_to_file("could not understand audio")
        return "could not understand audio"
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        write_to_file("Sphinx error; {0}".format(e))
        return "Sphinx error; {0}".format(e)

def write_to_file(text):
    with open('notes.txt', 'w') as f:
        f.write(text)