import sys
import os
import json
import urllib.parse
import urllib.request

def analyze(texts):
    apikey = 'ec55681e9caaa80c977bfcadcbdb9bea'
    endpoint = 'https://api.gavagai.se/v3/tonality'

    text_payload = [{'body': t, 'id': i} for i, t in enumerate(texts)]

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

    return as_json
