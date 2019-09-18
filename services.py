import urllib.request
import json


def random_facts() -> dict:
    try:
        with urllib.request.urlopen('https://uselessfacts.jsph.pl/random.json?language=en') as url:
            res = json.loads(url.read().decode())
            return {'text': res['text'], 'source': res['source_url']}
    except KeyError:
        return {}
