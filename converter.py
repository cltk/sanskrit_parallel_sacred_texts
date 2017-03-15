import os, re
import json
import pdb
import collections
from django.utils.text import slugify

sourceLink = 'http://sacred-texts.com/hin/index.htm'
source = 'Scared_Text_Archive'

def main():
    if not os.path.exists('cltk_json'):
        os.makedirs('cltk_json')

    for root, dirs, files in os.walk("."):
        path = root.split('/')
        for fname in files:
            if fname.endswith('txt'):
                #print((len(path) - 1) * '---', os.path.basename(root))
                language = 'Not Known'
                if '_eng.txt' in fname:
                    language = 'English'
                elif '_sans.txt' in fname:
                    language = 'Sanskrit'
                title = fname.split('.htm')[0].title()
                work = {
                            'originalTitle': title,
                            'englishTitle': title,
                            'author': "Not Available",
                            'source': source,
                            'sourceLink': sourceLink,
                            'language': language,
                            'text': {},
                        }
                text = open(os.path.join(root, fname)).read().splitlines()
                text = [textNode.strip() for textNode in text if len(textNode.strip())]
                for i, textNode in enumerate(text):
                    work['text'][i] = textNode
                
                fname = slugify(work['source']) + '__' + slugify(work['englishTitle']) + '__' + slugify(work['language']) + '.json'
                fname = fname.replace(" ", "")
                with open('cltk_json/' + fname, 'w') as f:
                    json.dump(work, f)

if __name__ == '__main__':
    main()