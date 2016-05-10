import sys
import json
import urllib.parse
import urllib.request

def analyze(text, id):
    apikey = '97206d6e38358170e97b3600b84cbc62'
    endpoint = 'https://api.gavagai.se/v3/tonality'
    payload = {
        "language": "en",
        "texts": [
        {
          "body": text,
          "id": id
        }
      ]
    }

    json_data = json.dumps(payload).encode('utf8')
    query_string = {'apiKey': apikey}

    url = '{0}?{1}'.format(endpoint, urllib.parse.urlencode(query_string))

    headers = {'Content-Type': 'application/json'}


    request = urllib.request.Request(url, data=json_data, headers=headers)
    response = urllib.request.urlopen(request).read()

    return response
