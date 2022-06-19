import random
from english_words import english_words_lower_alpha_set

class IDGenerator():
    # Source: https://betterprogramming.pub/how-to-write-your-own-password-generator-in-python-2511e633cf53
    def get_words(self, word_path):
        '''
        function returning a list of words based on a text file.
        return type: list
        '''
        word_file = word_path
        with open(word_file,'r') as file:
            word_list = list(file) #creates a list incl. /newline
        return word_list

    def generate_random_words(self, word_source, word_count):
        '''
        function generating a list of random words based on a word source list
        and amount of words requested.
        return type: list
        '''
        password_words =[]
        for words in range(0,word_count):
            random_index = random.randint(0,len(word_source)-1)
            password_words.append(word_source[random_index])

        return password_words

    def generate_random_number(self, padding):
        '''
        function returning a random number with a length determined by padding.
        fortmat will be able to return a number with leading 0s, hence its return value
        return type: string
        '''
        password_number = ''
        padding_count = 0
        while padding_count < padding:
            random_number = str(random.randint(0,9))
            password_number += random_number
            padding_count += 1
        return password_number

    def _generate_aerobridge_id(self, all_words, word_count, separator):
        '''
        funtion that returns a password based on user input
        all_words: a list containing strings
        word_count: how many words we want
        separator: how the separator looks.
        padding: padding for our random number
        special: optional if we want special character or not in our password
        special_amount: how many special characters we want.
        append order: words-number-special
        return type string
        '''
        new_id = self.generate_random_words(all_words,word_count)
        return (separator.join(new_id))
    
    def generate_aerobridge_id(self):
        return self._generate_aerobridge_id(list(english_words_lower_alpha_set),3,'_')
