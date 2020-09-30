#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import unicodedata


def Text(text):
    """ provide a wrapper for python string
    map byte to str (python 3)
    all string in utf-8 encoding
    normalize string to NFC
    """
    if not is_unicode(text):
        text = text.decode("utf-8")
    text = unicodedata.normalize("NFC", text)
    return text


def is_unicode(text):
    return type(text) == str


UPCASE_CHARACTERS = "QWERTYUIOPASDFGHJKLZXCVBNMÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ"
LOWCASE_CHARACTERS = UPCASE_CHARACTERS.lower()

specials = [r"==>", r"->", r"\.\.\.", r">>", r"=\)\)"]
digit = r"\d+([\.,_]\d+)+"
email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# urls pattern from nltk
# https://www.nltk.org/_modules/nltk/tokenize/casual.html
# with Vu Anh's modified to match fpt protocol
urls = r"""             # Capture 1: entire matched URL
  (?:
  (ftp|http)s?:               # URL protocol and colon
    (?:
      /{1,3}            # 1-3 slashes
      |                 #   or
      [a-z0-9%]         # Single letter or digit or '%'
                        # (Trying not to match e.g. "URI::Escape")
    )
    |                   #   or
                        # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:[a-z]{2,13})
    /
  )
  (?:                                  # One or more:
    [^\s()<>{}\[\]]+                   # Run of non-space, non-()<>{}[]
    |                                  #   or
    # balanced parens, one level deep: (...(...)...)
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)
    |
    \([^\s]+?\)                        # balanced parens, non-recursive: (...)
  )+
  (?:                                  # End with:
    # balanced parens, one level deep: (...(...)...)
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)
    |
    \([^\s]+?\)                        # balanced parens, non-recursive: (...)
    |                                  #   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]     # not a space or one of these punct chars
  )
  |                        # OR, the following to match naked domains:
  (?:
    (?<!@)                 # not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:[a-z]{2,13})
    \b
    /?
    (?!@)                  # not succeeded by a @,
                           # avoid matching "foo.na" in "foo.na@example.com"
  )
"""
datetime = [
    # Thông tư 58/2020
    r"\d{1,4}\/\d{4}",
    # 01/1/2014 , 1/1
    r"\d{1,2}\/\d{1,2}(\/\d+)?",
    r"\d{1,2}-\d{1,2}(-\d+)?",
]

word = r"\w+"
non_word = r"[^\w\s]"
abbreviations = [
    r"Tp\.",
    r"BS\.",
    r"BS\.",
    r"U\.S",
    r"Mr\.",
    "Mrs\.",
    "Ms\.",
    r"Dr\.",
    "ThS\.",
    r"TP\.",
]

special_names = [
    r"[A-Za-z]+s\'",
    r"[a-z]+-[A-Z]{1}\w+",  # al-Hajar, bin-Laden
    r"[A-Z]+[-]{1}[A-Za-z0-9]+",  # M&A , T&H
    r"[A-Z]+[&]{1}[A-Z]+",  # M&A , T&H
    r"[A-Z]{1,2}[-+]{1}",  # K+ , nhóm máu A+ , A-, RH+
    r"[A-Z]+\d+\.\d+",  # A2.0 , SA2.0,
]

cus_hyphen = [
    # biển số xe: 29H-116.87, 30E-180.54
    r"[0-9A-Z]{3,5}[\-]{1}[.0-9]{3,6}",
    r"d\'\w+",
    # # H'Mông, Đắc'Rong, Ê'Đê ...
    r"\w+\'\w+",
    # hyphen, F-16, Su-8, Apolo-2 ,H-Capital, A-Apolo  Nano-Bio ...
    # r'[A-Z]{1}[A-Za-z0-9]*[-]{1}[A-Za-z0-9]+'
    r"[A-Z]{1}[A-Za-z0-9]*[-]{1}\w+",
]

units = [
    r"(người)[/\\]{1}(km²)",
    r"(lít)[/\\]{1}(m²|m2|ha|m³)",
    r"(m|cm|km)[/\\]{1}(giờ|phút|giây)",
    r"^\d+(.\d+)?(%|km|kg)",
]

patterns = []
patterns.extend(special_names)
patterns.extend(units)
patterns.extend(cus_hyphen)
patterns.extend(datetime)
patterns.extend(abbreviations)
patterns.extend(specials)
patterns.extend([urls])
patterns.extend([email])
patterns.extend([digit])
patterns.extend([non_word])
patterns.extend([word])


patterns = "(" + "|".join(patterns) + ")"
if sys.version_info < (3, 0):
    patterns = patterns.decode("utf-8")
patterns = re.compile(patterns, re.VERBOSE | re.UNICODE)


def tokenize(text, format=None):
    """
    tokenize text for word segmentation

    :param text: raw text input
    :return: tokenize text
    """
    text = Text(text)
    text = text.replace("\t", " ")
    tokens = re.findall(patterns, text)
    tokens = [token[0] for token in tokens]
    if format == "text":
        return " ".join(tokens)
    else:
        return tokens


if __name__ == "__main__":
    s = "Midi-Pyrénées, người/km²,km²,U.S, bin-Ladem ,Trung Lương-Mỹ Thuận, Dar al-Hajar vốn là nơi ở mùa hè của , ngày 30/6/2018, Zozibini, BS.Hê Thanh Nhã Yến, sân St James' Park, Thông tư 58/2020, 45.5%, 30km,50.2kg,Dar al-Hajar, VN-Index Honda WR-V 2020 giá từ 11.300 USD.vô địch La Liga. C.T Group lọt 3 mong HCM. M&A, Lux A2, Fadil, Lux A2.0 và Lux SA2.0, Brooklyn Beckham, K+, nhóm máu RH+, RH- ĐH KHXH&NV 120 km/h ti số  2-0 'la sao'. biển kiểm soát 30E-180.54 đi với tốc độ nhanh, lạng lách, làm xe tải biển 29H-116.87 lật ngang 2 phương thức tuyển sinh của Đại học Hùng Vương TP HCM. Trường 20/09/2019 http://google.com/?index=1"
    match = patterns.findall(s)
    print(match)
    print(tokenize(s))
