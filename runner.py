import os
import re
import main

okay = 0

for file in os.listdir('samples'):
    if file.endswith('.wav'):
        if re.split(r"\W+|_", file)[1] == main.verify_speaker_gender("samples/" + file):
            okay += 1
print("%d/%d" % (okay, os.listdir('samples').__len__()))