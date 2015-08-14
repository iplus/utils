import datetime
import sys
import itertools
import heapq

class Line(object):
    def __init__(self, when, text):
        self.when = when
        self.text = text

    def __lt__(self, other):
        return self.when < other.when

    def __repr__(self):
        return self.text


def srt_file_producer(file_name):
    with open(file_name, 'r') as f:
        while True:
            if not f.readline():
                break
            txt = ''
            s = f.readline()
            when = s.split(' ')[0]  # 00:00:01,648 --> 00:00:05,594
            when = datetime.datetime.strptime(when, '%H:%M:%S,%f')
            while s and s != '\n':
                txt += s
                s = f.readline()
            yield Line(when, txt)


def combine_srt_files(file_names):
    srt_files = map(srt_file_producer, file_names)
    return heapq.merge(*srt_files)

ind = itertools.count(1)
for line in combine_srt_files(sys.argv[1:]):
    print(next(ind))
    print(line)