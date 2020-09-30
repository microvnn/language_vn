from word_tokenize.WordSegmenter import WordSegmenter
from sent_tokenize import sent_tokenize


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
        # 'Hồ Bán Nguyệt',
        # 'tượng đài Mẹ Suốt',
        # 'Công viên Thương Bạc',
        # 'tham quan Tháp Bà Ponagar',
        # 'Hồ Ngọc Hà',
        # 'nhà thờ Con Gà Đà Nẵng',
        "Hồ Con Rùa",
        # 'Trường Sĩ quan Phòng hóa',
        # 'nhà thờ Con Gà Đà Nẵng',
        # 'Trường hợp Mỹ quan ngại',
        # 'Mỹ quan thành phố',
        # 'Mỹ quan tâm',
        # 'bắc qua Hoàng Xuyên Tam Hiệp tại Liên Châu',
        # 'Mai Trung Hậu',
        # "Đức Tiến chăm con",
        # "phim Đức Tiến chăm con",
        # 'thủ tướng Đức Mike Ala',
        # 'tổng thống Mỹ Donal Trumb',
        # 'Chủ tịch Hà Nội Nguyễn Đức Chung',
        # 'Thêm 2 người bị khởi tố vì giúp đại gia Trịnh Sướng',
        # 'Mai Trung Hậu, 36 tuổi, và Trương Như Tuyết, 42 tuổi',
        # 'UBND xã Hoàng Long Cháu Ông Trời tại Long Châu',
        # 'Đại học Hùng Vương TP HCM',
        # 'Tiến sĩ Hà Xuân Linh, Trưởng Khoa Quốc tế, Đại học Thái Nguyên cho biết',
        # 'Chủ tịch UBND xã Hương Long Nguyễn Quốc Việt cho biết'
        # "Chương trình 'Thứ 4 - ngày cười' của Công ty Du lịch Á Châu"
        # 'Lãnh đạo tỉnh Bình Định thống nhất cấm đậu, đỗ xe trên tuyến đường Xuân Diệu, Nguyễn Tất Thành để tổ chức giải chạy diễn ra ngày 26/7 tới.hạy diễn ra ngày 26/7 tới.    '
    ]
    for x in word_tokenize(ss, format="text", multiline=True):
        print(x)
        print("---")
