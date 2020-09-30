import re
PHRASE_IN_QUOTE = re.compile(r"\"(.*?)\"|\'(.*?)\'")
words_by_pass = ["theo", "bộ", "sở", "cục", "hồ", "sông", "suối", "đảo",
                 "quận", "huyện", "xã", "thị trấn"]
BY_PASS_RULE = re.compile(r'(\s+|^)(%s)' % '|'.join(words_by_pass))
# BY_PASS_RULE = re.compile(r'dm')
PUNCT_QUOTE = re.compile(
    "/\\*|,|\\.|:|\\?|!|;|_|\"|'|“|”|\\|\\(|\\)|\\[|\\]|\\{|\\}|\\\\|\\/|¦|…|‘|’|·")
PUNCTUATION_FIXED = re.compile(
    "(\\.\\.\\.|\\)|\\(|:|\\?|!|;|\"|“|”|…|‘|’|·|'$|^')")

words_reaplces = [
    ("òa", "oà"),
    ("óa", "oá"),
    ("ỏa", "oả"),
    ("õa", "oã"),
    ("ọa", "oạ"),
    ("òe", "oè"),
    ("óe", "oé"),
    ("ỏe", "oẻ"),
    ("õe", "oẽ"),
    ("ọe", "oẹ"),
    ("ùy", "uỳ"),
    ("úy", "uý"),
    ("ủy", "uỷ"),
    ("ũy", "uỹ"),
    ("ụy", "uỵ"),
    ("Ủy", "Uỷ")
]


def match_to_str(match):
    quote = match.group()[0]
    s = (match.group()[1:len(match.group())-1]).strip()
    if s is None or len(s) < 1:
        return match.group()
    if BY_PASS_RULE.search(s):
        return match.group()
    vaild = True if PUNCT_QUOTE.search(s) is None else False
    if '-' in s:
        vaild = False
    if not vaild:
        return match.group()
    length = len(s.split())
    if vaild and length < 7 and s[0].istitle():
        return '%s %s %s' % (quote, s.replace(' ', '_'), quote)
    elif vaild and length < 4:
        return '%s %s %s' % (quote, s.replace(' ', '_'), quote)
    return match.group()


def getStringsInRule(s: str):
    return PHRASE_IN_QUOTE.sub(lambda x: match_to_str(x), s)
    # get_rule


def normalize_str(s):
    for x, y in words_reaplces:
        s = s.replace(x, y)
    s = PHRASE_IN_QUOTE.sub(lambda x: match_to_str(x), s)
    s = PUNCTUATION_FIXED.sub(lambda x: ' %s ' % x.group(), s)
    s = PUNCTUATION_FIXED.sub(lambda x: ' %s ' % x.group(), s)
    s = s.replace('_', ' ')
    return s


if __name__ == '__main__':
    # print(normalize_str("sân St James' Park ở vòng 36 Ngoại hạng Anh. 'Chào thân ái'"))
    print(normalize_str('chương trình "Giảm 300 - Bay vạn dặm"'))
    # print(normalize_str(' Né tránh \'chuyện ấy\' khi chưa sẵn sàng'))
    # print(BY_PASS_RULE.search('chuyện ấy'))
