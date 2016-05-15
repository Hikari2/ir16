import speech_text
import os
import tonality

def main(args):
    text = args[0]
    print('Analyzing...')
    file = args[1]
    result = tonality.analyze(text, file)

    print('Done!')
	      
    print(result)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
