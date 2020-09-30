# -*- coding: utf-8 -*-

import io
import json
import csv


def get_writer(filename, delimiter="\t", mode="w"):
    out = open(filename, mode, encoding="utf-8", newline="")
    writer = csv.writer(out, delimiter="\t", quoting=csv.QUOTE_MINIMAL, escapechar="\\")
    return writer, out


def write_csv(filename, rows, delimiter="\t", mode="w"):
    out = open(filename, mode, encoding="utf-8", newline="")
    writer = csv.writer(out, delimiter="\t", quoting=csv.QUOTE_MINIMAL, escapechar="\\")
    writer.writerows(rows)
    out.close()


def readlines_csv(filename, delimiter="\t"):
    f = io.open(filename, "r", encoding="utf-8")
    reader = [X for X in csv.reader(f, delimiter=delimiter)]
    f.close()
    return reader


def readlines(filename):
    f = io.open(filename, "r", encoding="utf-8")
    return [x.strip() for x in f.readlines()]


def read(filename):
    with io.open(filename, "r", encoding="utf-8") as f:
        text = f.read()
        f.close()
    return text


def write(filename, text):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.close()


def read_json(filename):
    with io.open(filename, "r", encoding="utf-8") as f:
        js = json.load(f)
        f.close()
    return js


def write_json(filename, data):
    with io.open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        f.close()
