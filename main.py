import speech_text
import os
import tonality
import sys
import numpy as np
import subprocess
from review_input import GROUPS

USED_FIELDS = ['positivity', 'negativity']
N = [5,10,15,20,25,30]

USE_SUBPROCESS = not 'windows' in [arg.lower() for arg in sys.argv]

MEGA_QUERY = True
TIGHT_PRINT = True

def main():

    # Only uses one gavagai query to reduce request numbers
    if MEGA_QUERY == True:
        sentences = []
        for group in GROUPS:
            for n in N:
                brands = [[name.lower() for name in g] for g in group["brands_grouped"]]
                for brand in brands:
                    text = speech_text.translate('audio/'+group["file"]+'.wav')
                    sentences += extract_sentences(text, brand, n)
        tonality.analyze(sentences) # Uses one query for all senctences and caches the results on disk

    for group in GROUPS:
        print()
        print()
        print(" --------- ANALYSING %s ---------"%group["file"])
        for n in N:
            if not TIGHT_PRINT:
                print()
                print("RESULTS FOR N = %s"%n)
            run_analyse(group, n)

def run_analyse(group, n):
    text = speech_text.translate('audio/'+group["file"]+'.wav')

    if USE_SUBPROCESS:
        brands = group["brands"]
    else:
        brands = [[name.lower() for name in g] for g in group["brands_grouped"]]

    
    for brand in brands:
        # Split into n-grams or whatever here
        if USE_SUBPROCESS:
            sentences = extract_sentences_grep(group["file"], brand)
        else:
            sentences = extract_sentences(text, brand, n)

        if sentences:
            result = tonality.analyze(sentences)
                
            # Get the fields we are interested in
            scores = [extract_scores(sentiments) for sentiments in result["texts"]]

            # Calculate the final sentiment
            verdict = extract_aggregate(scores)

            if not TIGHT_PRINT:
                print("--- RESULTS FOR %s ---"%brand)
                for key, value in verdict.items():
                    print(key, value)
            else:
                best = "Postive" if verdict["positivity"]['score'] > verdict["negativity"]['score'] else "Negative"
                print("%s\tN=%s | %s | P %s | N %s"%(brand,n,best,"{0:.2f}".format(verdict["positivity"]['score']),"{0:.2f}".format(verdict["negativity"]['score'])))
        else:
            print("Found no mentions of %s"%brand)

# Extract sentences containing brand name
# Using Unix command shell
def extract_sentences(filename, brand):
    try:
        grepResult = subprocess.check_output(['grep', '-i', brand.strip(), 'text_to_speech/'+filename+'.txt'], universal_newlines=True)
        sentences = grepResult.splitlines()
        return sentences
    except:
        return

# Extract sentences containing brand name
def extract_sentences(text, brands, n):
    words = [word.lower() for word in text.split()]
    sentences = []
    for i, word in enumerate(words):
        if word in brands:
            scope = (max(i-n,0), min(len(words)-1,i+1+n))
            sentence = " ".join(words[scope[0]:scope[1]])
            sentences.append(sentence)
    return sentences


# The aggregate function for all sentences
def extract_aggregate(sentiment_list):
    # Currently only an average

    # Combine all tones with same name:
    # negativity: {'score': [1.0, 0.0], 'normalizedScore': [0.5, 0.0]}
    # etc
    split_by_key = {}
    for s in sentiment_list:
        for tone in s["tones"]:
            field = tone["tone"]
            for k,v in tone.items():
                if k == "tone":
                    continue
                if split_by_key.get(field) == None:
                    split_by_key[field] = {}
                if split_by_key[field].get(k) == None:
                    split_by_key[field][k] = []
                split_by_key[field][k].append(v)

    # The Aggregation
    aggregated_keys = {}
    for k,v in split_by_key.items():
        aggregated_keys[k] = {}
        for k2,v2 in v.items():
            aggregated_keys[k][k2] = np.mean(v2)

    return aggregated_keys


# Extracts the relevant scores from a sentiment text
def extract_scores(sentiment):
    tonality = [value for value in sentiment["tonality"] 
                                if value['tone'] in USED_FIELDS]
    return {"id": sentiment["id"], "tones": tonality}


# Print the extracted scores of used fields
def pretty_print_scores(scores):
    for score in scores:
        print("")
        for s in score[1]:
            print(score[0], s)

# Print the json tree for the response
def pretty_print_response(response):
    for sentiments in response["texts"]:
        for key, values in sentiments.items():
            if key == "id":
                print("id:", values)
            else:
                for value in values:
                    print(key,value)


if __name__ == '__main__':
    main()