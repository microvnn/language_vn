# -*- coding: utf-8 -*-

from word_tokenize.sc_rdr.SCRDRTree import SCRDRTree
from word_tokenize.utility.rules import normalize_str
from os import path
from word_tokenize.regex_tokenize import tokenize
from word_tokenize.sc_rdr.WordTag import WordTag
from word_tokenize.vocabulary import Vocabulary
from word_tokenize.sc_rdr.Object import FWObject
from word_tokenize.sc_rdr.Node import Node
from util.singleton import Singleton
import re

vocabulary: Vocabulary = Vocabulary.Instance()
RESULT_SCORE = re.compile("\\d+([%])?-\\d+([%])?")


@Singleton
class WordSegmenter:
    def __init__(self, debug=False):
        cdr_file = path.join(path.dirname(__file__), "data", "wordsegmenter.rdr")
        self.__root = SCRDRTree()
        self.__root.constructSCRDRtreeFromRDRfile(cdr_file)
        self.__debug = debug

    def __findFiredNode(self, object: FWObject):
        currentN: Node = self.__root.root
        firedN: Node = None
        while True:
            if currentN.satisfy(object):
                firedN = currentN
                if currentN.getExceptNode() is None:
                    break
                else:
                    currentN = currentN.getExceptNode()
            else:
                if currentN.getIfnotNode() is None:
                    break
                else:
                    currentN = currentN.getIfnotNode()
        return firedN

    def __init_segmentation(self, sentence):
        sentence = normalize_str(sentence)
        tokens = tokenize(sentence)
        lowerTokens = [x.lower() for x in tokens]
        # print('tokens: ', tokens)
        # print('lowerTokens: ', lowerTokens)
        senLength, i = len(tokens), 0
        wordtags = []

        HARD_DICT = vocabulary.get_hard_dict()
        VN_DICT_UGRAM = vocabulary.get_vn_dict_ugram()
        LOCATION = vocabulary.get_location()
        VN_DICT = vocabulary.get_vn_dict()
        GIVEN_NAME = vocabulary.get_given_name()
        FIRST_SENT_WORDS = vocabulary.get_first_sent_word()
        MIDDLE_NAMES = vocabulary.get_middle_names()
        FAMILY_NAMES = vocabulary.get_family_names()

        while i < senLength:
            token: str = tokens[i]
            if "_" in token:
                wordtags.append(WordTag(token, "B"))
                i += 1
                continue

            if (token[0].islower() and (i + 1) < senLength) and tokens[i + 1].istitle():
                wordtags.append(WordTag(token, "B"))
                i += 1
                continue

            isSingleSyllabel = True
            max_ugram, in_hard_dict, hard_dic = 4, False, None
            if i <= senLength - max_ugram:
                word_start_ugram = " ".join(lowerTokens[i : i + 2])
                if word_start_ugram in VN_DICT_UGRAM:
                    # print("word_start_ugram: ", word_start_ugram)
                    max_ugram = vocabulary.max_ugram
                if token[0].isupper() and word_start_ugram in HARD_DICT:
                    in_hard_dict = True
                    hard_dic = HARD_DICT.get(word_start_ugram)

            if in_hard_dict:
                found_hard_dict = False
                # print("start_word in HARD_DICT: ", hard_dic)
                for j in range(min([i + hard_dic.max_len, senLength]), 1, -1):
                    word = " ".join(lowerTokens[i:j])
                    if word in hard_dic.data:
                        wordtags.append(WordTag(token, "B"))
                        for k in range(i + 1, j):
                            wordtags.append(WordTag(tokens[k], "I"))
                        i = j
                        found_hard_dict = True
                        break
                if found_hard_dict:
                    continue

            #
            for j in range(min([i + max_ugram, senLength]), 1, -1):
                word = " ".join(lowerTokens[i:j])
                is_capital = True
                for t in tokens[i:j]:
                    #  add Rule : 737 MAX (Number + ALL_UC)
                    if not t[0].isdigit() and t != "và" and not t[0].istitle():
                        is_capital = False
                        break
                if word in VN_DICT or (is_capital and word in GIVEN_NAME):
                    wordtags.append(WordTag(token, "B"))
                    for k in range(i + 1, j):
                        wordtags.append(WordTag(tokens[k], "I"))
                    i = j - 1
                    isSingleSyllabel = False
                    break
                elif is_capital and word in LOCATION:
                    # Xu ly rieng location
                    wordtags.append(WordTag(token, "B"))
                    for k in range(i + 1, j):
                        wordtags.append(WordTag(tokens[k], "I"))
                    i = j - 1
                    isSingleSyllabel = False
                    break

            if isSingleSyllabel:
                lower_token = lowerTokens[i]
                if lower_token.isalpha():
                    if (
                        lower_token in FIRST_SENT_WORDS
                        or token[0].islower()
                        or token.isupper()
                        or lower_token in GIVEN_NAME
                    ):
                        wordtags.append(WordTag(token, "B"))
                        i += 1
                        continue

                    #  Capitalized
                    ilower = i + 1
                    for ilower in range(i + 1, min([i + 7, senLength]) + 1):
                        if ilower >= senLength:
                            break
                        ntoken: str = tokens[ilower]
                        if token.isupper():
                            break
                        elif not ntoken.istitle():
                            break
                        elif "-" in ntoken and len(ntoken) > 1:
                            if RESULT_SCORE.search(ntoken):
                                break
                            elif not ntoken.replace("-", "").isalpha():
                                break
                        elif not ntoken.isalpha():
                            break

                    if ilower > i + 1:
                        isNotMiddleName = True
                        if lower_token in MIDDLE_NAMES and i > 0:
                            prevT: str = tokens[i - 1]
                            if prevT[0].isupper() and prevT.lower() in FAMILY_NAMES:
                                wordtags.append(WordTag(token, "I"))
                                isNotMiddleName = False

                        if isNotMiddleName:
                            wordtags.append(WordTag(token, "B"))
                        for k in range(i + 1, ilower):
                            wordtags.append(WordTag(tokens[k], "I"))
                        i = ilower - 1
                    else:
                        wordtags.append(WordTag(token, "B"))
                else:
                    wordtags.append(WordTag(token, "B"))
            i += 1
        # if self.__debug:
        # for x in wordtags:
        #     print(x)
        return wordtags

    def tokenize(self, sentence):
        strings = []
        wordtags = self.__init_segmentation(sentence)
        size = len(wordtags)
        arr = []
        for i in range(0, size):
            obj: FWObject = FWObject.getFWObject(wordtags, i)
            firedNode: Node = self.__root.findFiredNode(obj)
            # print(obj)
            if firedNode.getDepth() > 0:
                wordtags[i].setTag(firedNode.getConclusion())
        for i in range(0, size):
            if wordtags[i].tag == "B":
                strings.append(" " + wordtags[i].form)
            else:
                strings.append("_" + wordtags[i].form)
        return "".join(strings).strip()

