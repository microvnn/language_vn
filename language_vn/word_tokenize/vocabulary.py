# -*- coding: utf-8 -*-

import logging
import re

#
from os import path
from util.io import readlines, write
from util.singleton import Singleton

whitespace = re.compile(r" +")

words_slip_given_name = [
    "tịch",
    "thống",
    "tá",
    "đốc",
    "tướng",
    "trưởng",
    "thư",
    "trấn",
    "xã",
    "quận",
    "huyện",
    "phường",
    "ấp",
    "học",
    "đẳng",
    "đạo",
    "cầu",
    "vượt",
    "treo",
    "ngã",
    "tư",
    "đường",
]


def normalize(word):
    return whitespace.sub(" ", word.replace("_", " ")).lower()


@Singleton
class Vocabulary:
    def __init__(self):
        self.__cur_dir = path.join(path.dirname(__file__), "data")
        self.__vn_dict = None
        self.__short_word = None
        self.__location = None
        self.__location_lv_3 = None
        self.__vn_dict_ugram = None
        self.__first_sent_word = None
        self.__family_names = None
        self.__middle_names = None
        self.__max_ugram = 4
        self.__given_names = None
        self.__hard_dict = None

    @property
    def max_ugram(self):
        return self.__max_ugram

    def write_append(self, word, filename):
        f = open(filename, mode="a+", encoding="utf-8")
        f.write("\n" + word)
        f.close()

    def add_hard_dict(self, word):
        # add to vocabulary_build:
        x = normalize(word)
        self.get_hard_dict()
        if x not in self.__hard_dict:
            filename = path.join(self.__cur_dir, "hard_dict.txt")
            self.write_append(word=word, filename=filename)
            self.__hard_dict.add(x)

    def get_hard_dict(self):
        if self.__hard_dict is None:
            filename = path.join(self.__cur_dir, "hard_dict.txt")
            logging.info("%s loaded" % filename)
            dic, sizeof = dict(), dict()
            arr = [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            for x in arr:
                sl = x.split()
                key = " ".join(sl[0:2])
                if key not in dic:
                    dic[key] = set([])
                    sizeof[key] = 0
                dic[key].add(x)
                if len(sl) > sizeof[key]:
                    sizeof[key] = len(sl)
            self.__hard_dict = dict()
            for i in dic:
                self.__hard_dict[i] = dict(max_len=sizeof.get(i), data=dic.get(i))

        return self.__hard_dict

    def get_middle_names(self) -> set:
        if self.__middle_names is None:
            filename = path.join(self.__cur_dir, "middle_names.txt")
            logging.info("%s loaded" % filename)
            arr = [normalize(x) for x in readlines(filename)]
            self.__middle_names = set(list(dict.fromkeys(arr)))
        return self.__middle_names

    def get_family_names(self) -> set:
        if self.__family_names is None:
            filename = path.join(self.__cur_dir, "family_names.txt")
            logging.info("%s loaded" % filename)
            arr = [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            self.__family_names = set(list(dict.fromkeys(arr)))
        return self.__family_names

    def get_first_sent_word(self) -> set:
        if self.__first_sent_word is None:
            filename = path.join(self.__cur_dir, "first_words.txt")
            logging.info("%s loaded" % filename)
            arr = [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            self.__first_sent_word = set(list(dict.fromkeys(arr)))
        return self.__first_sent_word

    def get_short_word(self) -> set:
        if self.__short_word is None:
            filename = path.join(self.__cur_dir, "short_words.txt")
            logging.info("%s loaded" % filename)
            arr = [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            self.__short_word = set(list(dict.fromkeys(arr)))
        return self.__short_word

    def get_vn_dict_ugram(self) -> set:
        if self.__vn_dict_ugram is None:
            arr = []
            for x in self.get_vn_dict():
                sl = x.split()
                if len(sl) > 8:
                    # print(x)
                    continue
                if len(sl) > 4:
                    arr.append(" ".join(sl[0:2]))
                if len(sl) > self.__max_ugram:
                    self.__max_ugram = len(sl)
            self.__vn_dict_ugram = list(dict.fromkeys(arr))
        return self.__vn_dict_ugram

    def add_custom_dict_vn(self, word):
        # add to vocabulary_build:
        x = normalize(word)
        self.get_vn_dict()
        if x not in self.__vn_dict:
            filename = path.join(self.__cur_dir, "vocabulary_build.txt")
            self.write_append(word=word, filename=filename)
            self.__vn_dict.add(x)

    def get_vn_dict(self) -> set:
        if self.__vn_dict is None:
            files = {
                "vocabulary_standard.txt",
                "vocabulary_build.txt",
                "vocabulary.txt",
                "animal.txt",
            }
            arr = []
            for f in files:
                filename = path.join(self.__cur_dir, f)
                logging.info("%s loaded" % filename)
                arr += [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            arr = list(dict.fromkeys(arr))
            self.__vn_dict = set(arr)
        return self.__vn_dict

    def add_given_name(self, word):
        # add to vocabulary_build:
        x = normalize(word)
        self.get_vn_dict()
        if x not in self.__given_names:
            filename = path.join(self.__cur_dir, "names.txt")
            self.write_append(word=word, filename=filename)
            self.__given_names.add(x)

    def get_given_name(self) -> set:
        if self.__given_names is None:
            files = {"names.txt", "company.txt"}
            arr = []
            for f in files:
                filename = path.join(self.__cur_dir, f)
                logging.info("%s loaded" % filename)
                arr += [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            arr = list(dict.fromkeys(arr))
            self.__given_names = set(arr)
        return self.__given_names

    def get_location_lv3(self):
        if self.__location_lv_3 is None:
            files = {"loc.lv3.txt"}
            arr = []
            for f in files:
                filename = path.join(self.__cur_dir, f)
                logging.info("%s loaded" % filename)
                arr += [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]

            arr = list(dict.fromkeys(arr))
            max_length = max([len(x.split()) for x in arr])
            self.__location_lv_3 = (max_length, set(arr))
        return self.__location_lv_3

    def get_location(self) -> set:
        if self.__location is None:
            files = {"loc.lv2.txt", "loc.lv2.fix.txt"}
            arr = []
            for f in files:
                filename = path.join(self.__cur_dir, f)
                logging.info("%s loaded" % filename)
                arr += [normalize(x) for x in readlines(filename) if len(x.strip()) > 0]
            arr = list(dict.fromkeys(arr))
            self.__location = set(arr)
        return self.__location


if __name__ == "__main__":
    vocal: Vocabulary = Vocabulary.Instance()
    dictionary = vocal.get_location_lv3()
    # print(list(dictionary)[:10])
    # print(list(vocal.get_vn_dict_ugram())[:4], len(vocal.get_vn_dict_ugram()))
    # vocal.add_custom_dict_vn('phí trước bạ aaaaaaaaaaaa')
    vocal.add_given_name("HungTH Test")
    vocal.add_hard_dict("HungTH 123")

