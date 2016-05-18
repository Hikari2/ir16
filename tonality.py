import sys
import os
import json
import urllib.parse
import urllib.request
from saved_gavagai import gavagai_analysis

first_run = [True]

def analyze(texts):
    apikey = '31dcf55cda2419477ca1f129953126d7'
    endpoint = 'https://api.gavagai.se/v3/tonality'

    # Remove new lines
    texts = [text.replace('\n',' ') for text in texts]

    text_payload = [{'body': t, 'id': i} for i,t in enumerate(texts) 
                                if t not in gavagai_analysis]

    saved = [(i,gavagai_analysis[t]) for i,t in enumerate(texts) if t in gavagai_analysis]

    if len(text_payload) > 0:
        if first_run[0]:
            print("GAVAGAI STATS:")
            print("Total: %s"%len(texts))
            print("Cached: %s"%len(saved))
            print("New: %s"%len(text_payload))
    
            first_run[0] = False
        else:
            for pay in text_payload:
                print(pay["body"])
            raise Exception("Caching failed")
        payload = {
            "language": "en",
            "texts": text_payload
        }

        json_data = json.dumps(payload).encode('utf8')
        query_string = {'apiKey': apikey}

        url = '{0}?{1}'.format(endpoint, urllib.parse.urlencode(query_string))

        headers = {'Content-Type': 'application/json'}
        request = urllib.request.Request(url, data=json_data, headers=headers)
        response = urllib.request.urlopen(request).read()

        # Parse to Json format
        as_string = response.decode("UTF-8")
        as_json = json.loads(as_string)
    else:
    #    print("all " + str(len(saved)) + " texts are saved")
        as_json = {"texts": []}
    
    # Save new
    with open("saved_gavagai.py", "+a") as f:
        for sentiments in as_json["texts"]:
            original_text = next(t["body"] for t in text_payload if str(t["id"]) == sentiments["id"])
            print('gavagai_analysis["' + original_text + '"]=' + str(sentiments["tonality"]),file=f)
            gavagai_analysis[original_text] = sentiments["tonality"]

    # Load local
    for entry in saved:
        as_json["texts"].append({"id": entry[0], "tonality": entry[1]})

    return as_json
