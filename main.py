import speech_text
import os
import tonality
import json
import numpy as np
import subprocess

USED_FIELDS = ['positivity', 'negativity']

AUDIO = 'TOP_5_GAMING_MICE_-_2015_Edition'


# Extract sentences containing brand name
def extract_sentences(text, brand):
    try:
        grepResult = subprocess.check_output(['grep', '-i', brand.strip(), 'text_to_speech/'+AUDIO+'.txt'], universal_newlines=True)
        sentences = grepResult.splitlines()
        return sentences
    except:
        return
        

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









print("Speech to text")
text = speech_text.translate('audio/'+AUDIO+'.wav')
print("Sentiment analysis")
# Iterate through brands
with open('brands.txt', 'r') as brands:
    for brand in brands:
        
        # Split into n-grams or whatever here
        sentences = extract_sentences(text, brand)

        if sentences:
            result = tonality.analyze(sentences)
                
            # Get the fields we are interested in
            scores = [extract_scores(sentiments) for sentiments in result["texts"]]

            # Calculate the final sentiment
            verdict = extract_aggregate(scores)

            print("--- RESULTS FOR %s---"%brand)
            for key, value in verdict.items():
                print(key, value)
