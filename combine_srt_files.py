import datetime
import sys


class Line(object):
    def __init__(self, when, text):
        self.when = when
        self.text = text

    def __lt__(self, other):
        return self.when < other.when

    def __repr__(self):
        return self.text


def read_srt_file(file_name):
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


def combine_srt_files(*file_names):
    srt_files = list(map(read_srt_file, file_names))
    phrases = []
    for srt_file in srt_files:
        phrases.append(next(srt_file))
    while phrases:
        phrase = min(phrases)
        ind = phrases.index(phrase)
        yield phrase
        try:
            phrases[ind] = next(srt_files[ind])
        except StopIteration:
            srt_files.remove(srt_files[ind])
            phrases.remove(phrase)


i = 0
for line in combine_srt_files(*sys.argv[1:]):
    i += 1
    print(i)
    print(line)

