from language_vn.word_tokenize.WordSegmenter import WordSegmenter
from language_vn.sent_tokenize import sent_tokenize


def nomalizer_document(doc):
    if type(doc) is str:
        ss = sent_tokenize(doc)
        return ss
    else:
        return doc


def token_to_text(x):
    return x.replace(" ", "_")


def word_tokenize(doc, format=None, multiline=False):
    sentences = nomalizer_document(doc)
    segmenter = WordSegmenter.Instance()
    lines = []
    for s in sentences:
        r = segmenter.tokenize(s)
        lines.append(r)
    if multiline:
        if format == "text":
            return lines
        else:
            return [x.split() for x in lines]
    else:
        if format == "text":
            return " ".join(lines)
        else:
            result = []
            for x in lines:
                result += x.split()
            return result


if __name__ == "__main__":
    ss = [
        "Ivanka - đệ nhất ái nữ quyền lực của Trump",
        "Hồ Con Rùa",
    ]
    for x in word_tokenize(ss, format="text", multiline=True):
        print(x)
        print("---")
