# -*- coding: utf-8 -*-

from word_tokenize.sc_rdr.WordTag import WordTag
from word_tokenize.vocabulary import Vocabulary

attributes = [
    'W-2', 'T-2',
    'W-1', 'T-1',
    'W', 'T',
    'W+1', 'T+1',
    'W+2', 'T+2',
    'F', 'F-1', 'F-2', 'F+1',
    'P'
]

words_loc_prefix = [
    'xã', 'trấn', 'phường', 'quận'
]

vocabulary: Vocabulary = Vocabulary.Instance()
length, LOCATION_LV3 = vocabulary.get_location_lv3()


class FWObject:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check=False):
        self.context = [None, None, None, None, None,
                        None, None, None, None, None,
                        None, None, None, None, None]
        if(check == True):
            i = 0
            while (i < 10):
                self.context[i] = "<W>"
                self.context[i + 1] = "<T>"
                i = i + 2
            self.context[10] = "<F>"  # suffix
            self.context[11] = "<F>"
            self.context[12] = "<F>"
            self.context[13] = "<F>"
            self.context[14] = "N"
        self.notNoneIds = []

    @staticmethod
    def getFWObject(wordTags, index):
        object = FWObject(True)
        word: WordTag = wordTags[index]
        object.context[4] = word.word
        object.context[5] = word.tag
        object.context[10] = word.format
        if not word.form.istitle():
            wordTags[index].setI_No(0)

        if index > 0:
            pre_word_1: WordTag = wordTags[index - 1]
            object.context[2] = pre_word_1.word
            object.context[3] = pre_word_1.tag
            object.context[11] = pre_word_1.format
            if word.form.istitle():
                wordTags[index].setI_No(pre_word_1.i_no+1)

        if index > 1:
            pre_word_2: WordTag = wordTags[index - 2]
            object.context[0] = pre_word_2.word
            object.context[1] = pre_word_2.tag
            object.context[12] = pre_word_2.format

        if index < len(wordTags) - 1:
            next_word_1: WordTag = wordTags[index + 1]
            object.context[6] = next_word_1.word
            object.context[7] = next_word_1.tag
            object.context[13] = next_word_1.format

        if index < len(wordTags) - 2:
            next_word_2: WordTag = wordTags[index + 2]
            object.context[8] = next_word_2.word
            object.context[9] = next_word_2.tag

        # kiem tra
        if index > 0:
            last_word = None
            if index == len(wordTags) - 1 and wordTags[index].i_no >= 3:
                # cuoi cau
                last_word = wordTags[index]
            elif wordTags[index].i_no == 0 and wordTags[index-1].i_no >= 3:
                # giua cau
                last_word = wordTags[index-1]
            if last_word is not None:
                last_w_index = index - last_word.i_no
                if last_w_index > 0:
                    prefix_word = wordTags[last_w_index-1]
                    if prefix_word.word in words_loc_prefix:
                        # print('>> last_word: ', last_word)
                        # print('>> prefix_word, ', prefix_word)
                        fr = last_w_index
                        to = last_w_index + last_word.i_no
                        # print('>> Kiem tra loc lv3: %s -> %s' % (fr, to))
                        for j in range(to, fr, -1):
                            text_word = ' '.join(
                                [x.word for x in wordTags[fr:j]])
                            # print('>> text_word: ', text_word)
                            if text_word in LOCATION_LV3:
                                # print('>> find loc lv3: ', text_word)
                                # print('>> change B: ', wordTags[j])
                                wordTags[j].setTag('B')
        return object

    def isSatisfied(self, fwObject):
        for i in range(len(attributes)):
            key = self.context[i]
            if (key is not None):
                if key != fwObject.context[i]:
                    return False
        return True

    def __str__(self):
        builder = []
        for i in range(len(attributes)):
            builder.append('%s=%s' % (attributes[i], self.context[i]))

        return 'FWObject(%s)' % ', '.join(builder)
