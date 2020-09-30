# -*- coding: utf-8 -*-
import pickle
import string
import re
from os.path import join, dirname

from nltk import PunktSentenceTokenizer

sentence_tokenizer = None
sent_regex = re.compile("(\n)")


def _load_model():
    global sentence_tokenizer
    if sentence_tokenizer is not None:
        return
    model_path = join(dirname(__file__), "st_kiss-strunk-2006_2019_01_13.pkl")
    with open(model_path, "rb") as fs:
        punkt_param = pickle.load(fs)

    punkt_param.sent_starters = {}
    abbrev_types = [
        "g.m.t",
        "e.g",
        "dr",
        "dr",
        "vs",
        "000",
        "mr",
        "mrs",
        "prof",
        "inc",
        "tp",
        "tp." "ts",
        "ths",
        "th",
        "vs",
        "tp",
        "k.l",
        "a.w.a.k.e",
        "t",
        "a.i",
        "</i",
        "g.w",
        "ass",
        "u.n.c.l.e",
        "t.e.s.t",
        "ths",
        "d.c",
        "ve…",
        "ts",
        "f.t",
        "b.b",
        "z.e",
        "s.g",
        "m.p",
        "g.u.y",
        "l.c",
        "g.i",
        "j.f",
        "r.r",
        "v.i",
        "m.h",
        "a.s",
        "bs",
        "c.k",
        "aug",
        "t.d.q",
        "b…",
        "ph",
        "j.k",
        "e.l",
        "o.t",
        "s.a",
    ]
    abbrev_types.extend(string.ascii_uppercase)
    for abbrev_type in abbrev_types:
        punkt_param.abbrev_types.add(abbrev_type)
    for abbrev_type in string.ascii_lowercase:
        punkt_param.abbrev_types.add(abbrev_type)
    sentence_tokenizer = PunktSentenceTokenizer(punkt_param)


def sent_tokenize(text):
    global sent_tokenizer
    _load_model()

    paragraphs = [x.strip() for x in sent_regex.split(text)]
    sentences = []
    for p in paragraphs:
        p = p.replace(" - ", " , ")
        ss = sentence_tokenizer.sentences_from_text(p)
        for s in ss:
            s = s.strip()
            if s.endswith("..."):
                sentences.append(s[0 : len(s) - 3] + " ...")
            elif s[-1] in "?!.":
                sentences.append(s[0 : len(s) - 1] + " " + s[-1])
            else:
                sentences.append(s + " .")
    return sentences


if __name__ == "__main__":
    ss = u"""

Mấy tháng gần đây , tuần nào báo chí Malaysia cũng có bài viết về các vụ cướp biển ở Malacca , các anh nên cẩn thận đấy ! ” . 

Ông này từng nhiều lần nhập cảnh vào Việt Nam ; hồ sơ vụ án có ảnh nhận dạng , email trao đổi qua lại với Cường ...     
TP Điện Biên Phủ : Kế toán Trung tâm bồi dưỡng chính trị bị điều xuống làm ... lao công    
Nhân sự mới TP. HCM , Đắk Nông , Sơn La. 

39 người trong xe container có thể đã chết cóng
Chuyên gia cho rằng nhiệt độ trong thùng xe container tại hạt Essex có thể xuống mức -25 độ C, khiến 39 người bên trong không thể sống sót.

"Đây là nhiệt độ thường được cài đặt trên xe container đông lạnh để bảo quản hàng hóa chở theo như hoa quả hoặc thực phẩm tươi. Họ chỉ cần để -5 độ C để làm lạnh, nhưng -25 là nhiệt độ hóa đông. Có rất ít hoặc không có cơ hội sống sót nếu bạn ở trong điều kiện đó trong bất kỳ khoảng thời gian nào", Richard Burnett, Giám đốc điều hành của Hiệp hội vận tải đường bộ hôm 23/10 cho biết.

Bình luận được Burnett đưa ra sau khi cảnh sát hạt Essex phát hiện chiếc xe container bên trong khu công nghiệp Waterglade, cách trung tâm thủ đô London 32 km với 39 thi thể ở thùng xe phía sau, bao gồm 38 người lớn và một thiếu niên. Truyền thông Anh cho biết trên xe có gắn máy lạnh Carrier.
    """
    print(sent_tokenize(ss))
