#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mbd
"""
# Make requests
import requests
# XML parser
import xml.etree.ElementTree as ET
# OS
import os, errno
# Regex library
import re
# Text-to-speech library
from gtts import gTTS as g


def removeStar(text):
    exp = "(\*)"
    t = re.sub(exp, '', text)
    return t

def removeOth(text):
    exp = "(\s:)"
    t = re.sub(exp, ', ', str(text))
    exp = ":"
    t = re.sub(exp, '', t)
    return t

# Your Meriam Webster Learners Dictionary api key
key = ""

# Define an input file name to read words from it
# Define an output file to write definition data
input_file = "words.txt"
output_file = "definitions.txt"

selections = []

# You may produce audio files and get word definitions at the same time.
# Or you may choose to do one of these operations seperately.
produce_audio = False
get_definitions = True

if produce_audio:
    # Create a directory to store audio 
    # files if it doesn't exist.
    try: 
        os.makedirs('audio')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

with open(input_file,"r") as f:
    words = f.read().splitlines()

for word in words:
    if produce_audio:
        try:
            # Create a text-to-speech object
            tts = g(text=word, lang='en')
            # Define relative path
            r_path = './audio/' + word + '.mp3'
            # Save the audio to the given path
            tts.save(r_path)

            print('[INFO] Audio is saved for the word {} at {}'.format(word,r_path))
        except Exception as e:
            raise e

    if get_definitions:
        # Create the full URI
        uri = "http://www.dictionaryapi.com/api/v1/references/learners/xml/" + str(word) + "?key=" + key
        # Get data           
        r = requests.get(uri)
        if r.status_code == 200:
            # Pre-process
            text = r.text.encode('ascii','ignore')
            # Definitions are stored in this list
            definitions = []

            # Parse xml
            tree = ET.fromstring(text)

            # Definition counter for each word
            count = 0

            print("Word : {}".format(word))

            # Extract data from XML
            for i, item in enumerate(tree.iter('entry')):
                w = removeStar(item.find('hw').text)
                if w == str(word):
                    # Part of speech
                    pos = item.find('fl').text
                    print(pos)
                    # Definitions
                    for j, dfn in enumerate(item.iter('dt')):
                        t = removeOth(dfn.text)
                        if t != '':
                            print("{}. {}".format(count,t))
                            count += 1

                            definitions.append((pos,t))
            selection = 0
            # If the word has definitions more than one 
            # user should make a selection.
            if len(definitions) > 1:
                selection = int(input("Select the definition:\n> "))

            pos = definitions[selection][0]
            dfn = definitions[selection][1]

            selections.append((word,dfn,pos))
        else:
            print("[ERROR] For word '{}' got status code {}".format(word,r.status_code))
    print('---------------------------------')
if get_definitions:
    # Write definition and POS values of each word to a file 
    with open(output_file,"w") as f:
        for word, dfn, pos in selections:
            f.write(word + "\t" + dfn + "\t" + pos + "\n")
        print("[INFO] Word definitions are written to the file {} successfully".format(output_file))


