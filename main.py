import speech_text
import tonality

file = 'sound.wav'

print('Converting...')

text = speech_text.translate(file)

print(text)
print('Analyzing...')

result = tonality.analyze(text, file)

print('Done!')
      
print(result)
