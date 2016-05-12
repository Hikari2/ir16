import speech_recognition as sr

def translate(file):
    # obtain path to file in the same folder as this script
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using IBM Speech to Text
    IBM_USERNAME = "49c8eb61-b39e-4fff-83f4-69cb9b587177"
    IBM_PASSWORD = "oy8PkRiX2sYL"
    try:
        result = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        print(result)
        print(" ")
        return result
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
