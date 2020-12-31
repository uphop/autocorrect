import re
import os
from collections import Counter
import pandas as pd
import logging
import json
from string_edits import StringEdits
from edit_distance import EditDistance

'''
Init and configuration
'''
logger = logging.getLogger('autocorrect-server')

DATA_FOLDER = 'data'
VOCAB_FILE = DATA_FOLDER + '/words_dictionary.json'
HISTORY_FILE = DATA_FOLDER + '/words_usage_history.txt'

# Provides a list of suggestes auto-corrections per word
class AutoCorrect:
    # Constructor
    def __init__(self, max_suggestions = 3):
        # load vocabulary
        self.vocab = self.load_vocabulary()

        # load word usage history
        self.history = self.load_history()

        # calculate word usage probability
        self.probs = self.get_probs(self.history)
        self.max_suggestions = max_suggestions

        self.string_edits = StringEdits()
        self.edit_distance = EditDistance()

    # Loads vocabulary from JSON file
    def load_vocabulary(self):
        data = None

        # check if vocab file exists
        if(os.path.exists(VOCAB_FILE)):
            # if so, lets try to load and parse
            with open(VOCAB_FILE) as json_file:
                data = json.load(json_file)

        return data

    # Loads history from text file
    def load_history(self):
        word_l = []

        # check if history file exists
        if(os.path.exists(HISTORY_FILE)):
            # if so, lets try to load and parse
            df = pd.read_csv(HISTORY_FILE, sep='\t',header=None)
            for index, row in df.iterrows():
                # preprocess and add to history list
                text_words = self.preprocess(row[0])
                word_l.extend(text_words)
        
        # return dictionary where key is the word and value is its frequency
        word_count_dict = Counter(word_l)
        return word_count_dict

    # Returns dictionary where keys are the words and the values are the probability that a word will occur
    def get_probs(self, word_count_dict):
        probs = {}
        
        m = sum(word_count_dict.values())
        for word in word_count_dict:
            probs[word] = word_count_dict.get(word, 0) / m

        return probs

    # Pre-processes a sentence
    def preprocess(self, text):
        # make lower case
        text_lowercase = text.lower()

        # split to words
        text_words = re.findall(r'\w+', text_lowercase)

        return text_words
    
    # Filter list of tuples with the most probable n corrected words and their probabilities
    def get_best_suggestions(self, suggestions):
        n_best = []
        for suggestion in suggestions:
            n_best.append((suggestion, self.probs.get(suggestion, 0)))
        n_best.sort(key=lambda tup: tup[1], reverse=True)

        filtered_suggestions = []
        for suggestion in n_best[:self.max_suggestions]:
            filtered_suggestions.append(suggestion[0])

        return filtered_suggestions

    # Return a list of tuples with the most probable n corrected words and their probabilities
    def get_suggestions(self, word):
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
           
        for word in word_l:
            # get list of suggestions for each word
            suggestions = self.get_suggestions(word)
            best_suggestions = self.get_best_suggestions(suggestions)

            # get min edit distance for each word / suggestion pair
            suggestions_with_distance = []
            for suggestion in best_suggestions:
                _, min_edit_distance = self.edit_distance.get_min_edit_distance(word, suggestion)
                suggestions_with_distance.append({suggestion: str(min_edit_distance)})
            
            autocorrect_result[word] = suggestions_with_distance
            
        return autocorrect_result