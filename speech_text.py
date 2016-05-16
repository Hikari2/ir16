import speech_recognition as sr
import os

def translate(file):
    #file = 'audio/Us_English_Broadband_Sample_2.wav'
    # obtain path to file in the same folder as this script
    from os import path
    full_path = path.dirname(path.realpath(__file__))
    name = path.splitext(path.basename(file))[0] + ".txt"
    AUDIO_FILE = path.join(full_path, file)

    directory = full_path + "/text_to_speech"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(directory+"/"+name):
        print(file + " is already processed, returning from disk")
        with open(directory+"/"+name,"r") as f:
            ret_str = ""
            for line in f:
                ret_str += line+"\n"
            return ret_str;


    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using IBM Speech to Text
    IBM_USERNAME = "49c8eb61-b39e-4fff-83f4-69cb9b587177"
    IBM_PASSWORD = "oy8PkRiX2sYL"
    try:        
        result = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        with open(directory+"/"+name,"w+") as f:
            print(str(result),file=f)
        return result
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
