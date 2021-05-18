import requests
import json


def main():
    print('Looking up your IP')
    resp = requests.get('https://ip.tdirc.workers.dev', headers={
        'Accept': 'application/json'
    })
    obj = json.loads(resp.text)
    print('Your IP:', obj['ip'])
    print('Your region:', obj['region'])
