import json
import logging

import logging
import os

logging.basicConfig()

result = {}

# with open('dictionaries/mit10k.txt') as f:
#     for line in f:
#         line = line.replace('\n','')
#         if len(line) >= 3:
#             result[line] = 1
# with open('dictionaries/mit10k.json', 'w') as f:
#     json.dump(result,f)

with open('dictionaries/letterboxed.txt') as f:
    for line in f:
        if line[0] == '#': # comment
            continue
        if line[0] == '\n':
            continue
        line2 = line.lower()
        line2 = line2.replace('\n','')
        line2 = line2.replace(',', '')
        if not line2.isalpha():
            logging.error("Unexpected character in word {} / line : {}".format(line2, line[:-1]))
        elif len(line2) >= 3:
            result[line2] = 1
        else:
            logging.warning("Discarded short word {}".format(line2))
# with open('dictionaries/letterboxed.txt','w') as f:
#     f.writelines([x+'\n' for x in result.keys()])
os.remove('dictionaries/letterboxed.json')
with open('dictionaries/letterboxed.json', 'a') as f:
    json.dump(result,f)
