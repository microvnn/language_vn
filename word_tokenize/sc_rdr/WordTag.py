import re
import string
from word_tokenize.vocabulary import Vocabulary

DATE_1 = re.compile(
    "\\b([12][0-9]|3[01]|0*[1-9])[-/.](1[012]|0*[1-9])[-/.](\\d{4}|\\d{2})\\b")
DATE_2 = re.compile("\\b(1[012]|0*[1-9])[-/.](\\d{4}|\\d{2})\\b")
DATE_3 = re.compile("\\b([12][0-9]|3[01]|0*[1-9])[-/.](1[012]|0*[1-9])\\b")
FROM_TO = re.compile('^(\\d{1,3}[%]?)[-]{1}(\\d{1,3}[%]?)$')

vocabulary: Vocabulary = Vocabulary.Instance()


class WordTag:
    def __init__(self, iword: str, itag: str):
        self.__form = iword
        self.__word = iword.lower()
        self.__tag = itag
        self.__format = '<F>'
        self.__i_no = 0

        if len(self.__form) == 1 and self.__form[0].isdigit():
            self.__format = 'NU'
        elif len(self.__form) == 1 and not self.__form in string.punctuation:
            self.__format = 'PUNCT'
        elif (self.__word.isdigit()):
            #  Unit or number
            self.__format = 'NU'
        elif FROM_TO.search(self.__word):
            self.__format = 'RA'
        elif DATE_1.search(self.__form) or \
                DATE_2.search(self.__form) or \
                DATE_3.search(self.__form):
            self.__format = 'DT'
        elif len(self.__word) > 1 and self.__form.isupper():
            if self.__word in vocabulary.get_short_word():
                self.__format = 'SW'
            else:
                self.__format = 'UC'
        elif len(self.__word) > 1 and self.__form.istitle():
            self.__format = "TI"

    def setTag(self, v):
        self.__tag = v

    def setI_No(self, v):
        self.__i_no = v

    @property
    def format(self):
        return self.__format

    @property
    def format(self):
        return self.__format

    @property
    def i_no(self):
        return self.__i_no

    @property
    def form(self):
        return self.__form

    @property
    def word(self):
        return self.__word

    @property
    def tag(self):
        return self.__tag

    def __str__(self):
        return 'WordTag(form=%s, word=%s, tag=%s, format=%s, i_no=%s)' % \
            (self.form, self.word, self.tag, self.format, self.__i_no)


if __name__ == '__main__':
    word = WordTag('MAX', 'Np')
    print(word)
