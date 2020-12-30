class StringEdits:
    def __init__(self):
        self.letters = 'abcdefghijklmnopqrstuvwxyz'

    # Returns a list of all possible strings obtained by deleting 1 character from word
    def delete_letter(self, word):
        split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        delete_l = [(L + R[1:]) for L, R in split_l if R]
        return delete_l

    # Returns a list of all possible strings with one adjacent charater switched
    def switch_letter(self, word):
        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        switch_l = [(L + R[1] + R[0] + R[2:]) for L, R in split_l if len(R) >= 2]
        return switch_l
    
    # Returns a list of all possible strings where we replaced one letter from the original word
    def replace_letter(self, word):
        split_l = [(word[:i], word[i:]) for i in range(len(word))]
        replace_set = set([(L + C + R[1:]) for L, R in split_l for C in self.letters])
        replace_set.discard(word)
        replace_l = sorted(list(replace_set))
        return replace_l

    # Returns a set of all possible strings with one new letter inserted at every offset
    def insert_letter(self, word):
        split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        insert_l = [(L + C + R) for L, R in split_l for C in self.letters]
        return insert_l

    # Returns a set of words with one possible edit
    def edit_one_letter(self, word):
        one_letter_l = []

        # add variations with replace
        replace_l = self.replace_letter(word)
        one_letter_l.extend(replace_l)
        
        # add variations with insert
        insert_l = self.insert_letter(word)
        one_letter_l.extend(insert_l)
        
        # add variations with delete
        delete_l = self.delete_letter(word)
        one_letter_l.extend(delete_l)
        
        # add variations woth switch
        switch_l = self.switch_letter(word)
        one_letter_l.extend(switch_l)
        
        edit_one_set = set(one_letter_l)

        return edit_one_set
    
    # Returns a set of strings with all possible two edits
    def edit_two_letters(self, word):
        edit_two_l = []

        # add single edit variations
        edit_one_l = list(self.edit_one_letter(word))
        edit_two_l.extend(edit_one_l)
        
        # add double edit variations for each previosly collected single edit variations
        for edit_one_word in edit_one_l:
            edit_one_l = list(self.edit_one_letter(edit_one_word))
            edit_two_l.extend(edit_one_l)

        edit_two_set = set(edit_two_l)
        
        return edit_two_set