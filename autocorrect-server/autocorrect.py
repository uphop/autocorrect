import re
import os
from collections import Counter
import logging
import json
from string_edits import StringEdits

'''
Init and configuration
'''
logger = logging.getLogger('autocorrect-server')

VOCAB_FOLDER = 'data'
VOCAB_FILE = VOCAB_FOLDER + '/words_dictionary.json'

# Provides a list of suggestes auto-corrections per word
class AutoCorrect:
    # Constructor
    def __init__(self):
        self.vocab = self.load_vocabulary()
        self.string_edits = StringEdits()

    # Loads vocabulary from JSON file
    def load_vocabulary(self):
        data = None

        # check if vocab file exists
        if(os.path.exists(VOCAB_FILE)):
            # if so, lets try to load and parse
            with open(VOCAB_FILE) as json_file:
                data = json.load(json_file)

        return data

    # Pre-processes a sentence
    def preprocess(self, text):
        # make lower case
        text_lowercase = text.lower()

        # split to words
        text_words = re.findall(r'\w+', text_lowercase)

        return text_words
    
    # Return a list of tuples with the most probable n corrected words and their probabilities
    def get_corrections(self, word):
        # init list of suggestions
        suggestions = []

        # check if this word is actually in a vocabulary; if so, just return an empty suggesttion
        if not word in self.vocab:
            # if the word is not in vocab, let's try with single edit variations
            edit_one_set = self.string_edits.edit_one_letter(word)
            edit_one_intersection = edit_one_set.intersection(self.vocab)
            if(len(edit_one_intersection) > 0):
                suggestions = list(edit_one_intersection)
            else:
                # if no luck with single edit variations, let's try with two edits' variations
                edit_two_set = self.string_edits.edit_two_letters(word)
                edit_two_intersection = edit_two_set.intersection(self.vocab)
                if(len(edit_two_intersection) > 0):
                    suggestions = list(edit_two_intersection)
                else:
                    # if no luck again, just return the same word
                    suggestions = [word]

        return suggestions

    
    ## Checks each word in text and returns a list of suggestions for each one
    def check_text(self, text):
        # init result
        autocorrect_result = {}

        # split into words
        word_l = self.preprocess(text)

        # get list of corrections for each word
        for word in word_l:
            autocorrect_result[word] = self.get_corrections(word)
            
        return autocorrect_result