import speech_recognition as sr

def translate(file):
    # obtain path to file in the same folder as this script
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using Sphinx
    try:
        return(r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
