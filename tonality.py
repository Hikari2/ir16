import sys
import os
import json
import urllib.parse
import urllib.request
from saved_gavagai import gavagai_analysis

def analyze(texts):
    apikey = '0657d10bf91d916f8b486bb8c1660151'
    endpoint = 'https://api.gavagai.se/v3/tonality'

    # Remove new lines
    texts = [text.replace('\n',' ') for text in texts]

    text_payload = [{'body': t, 'id': i} for i,t in enumerate(texts) 
                                if t not in gavagai_analysis]

    saved = [(i,gavagai_analysis[t]) for i,t in enumerate(texts) if t in gavagai_analysis]

    if len(text_payload) > 0:
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
        print("all " + str(len(saved)) + " texts are saved")
        as_json = {"texts": []}
    
    # Save new
    with open("saved_gavagai.py", "+a") as f:
        for sentiments in as_json["texts"]:
            original_text = next(t["body"] for t in text_payload if str(t["id"]) == sentiments["id"])
            print('gavagai_analysis["' + original_text + '"]=' + str(sentiments["tonality"]),file=f)

    # Load local
    for entry in saved:
        as_json["texts"].append({"id": entry[0], "tonality": entry[1]})

    return as_json
