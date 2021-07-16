import sys
import re

with open(sys.argv[1]) as f:
    lines = f.readlines()
lines = lines[4:]
duration_re = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3}) ')
anchor_re = re.compile(r'<[^>]*>')
detail_word_re = re.compile(r'^ ?([^<]+)')
detail_time_re = re.compile(r'^<(\d{2}:\d{2}:\d{2}\.\d{3})>')

class Subtitle:

    def __init__(self, start=None, end=None, content=None, detail=None):
        self.start = start
        self.end = end
        self.content = content if content else ''
        self.detail = detail
        self.detail_end = end if detail else None

    def __repr__(self):
        return '<Subtitle start=%s, end=%s, content=%s, detail=%s>' % (self.start, self.end, self.content.replace('\n', '\\n'), 'yes' if self.detail else 'no')

subs = []
for line in lines:
    line = line.strip('\r\n')
    match = duration_re.search(line)
    if match:
        start = match.group(1)
        end = match.group(2)
    else:
        if line == '' or line == ' ':
            continue
        if '</c>' in line:
            subs.append(Subtitle(start=start, end=end, content=anchor_re.sub('', line), detail=line))
        else:
            subs.append(Subtitle(start=start, end=end, content=line))

# Merge subtiles
i = 0
while i < len(subs) - 1:
    current = subs[i]
    _next = subs[i+1]
    if current.content == _next.content and current.end == _next.start:
        subs[i].end = _next.end
        if _next.detail:
            if current.detail is None:
                subs[i].detail = _next.detail
            else:
                raise ValueError
        del subs[i+1]
    else:
        i += 1

# Fix ends
for i in range(len(subs)):
    if subs[i].detail_end:
        subs[i].end = subs[i].detail_end

    if i < len(subs) - 1:
        if subs[i].end > subs[i+1].start:
            subs[i].end = subs[i+1].start

output = []
for sub in subs:
    if sub.detail:
        i = 0
        start = sub.start
        while i < len(sub.detail):
            match = detail_word_re.match(sub.detail[i:])
            if match:
                word = match.group(1)
                i += len(match.group(0))
                continue
            match = detail_time_re.match(sub.detail[i:])
            if match:
                time = match.group(1)
                output.append('\t'.join([start, time, word]))
                start = time
                i += len(match.group(0))
                continue
            match = anchor_re.match(sub.detail[i:])
            if match:
                i += len(match.group(0))
        output.append('\t'.join([start, sub.detail_end, word]))
    else:
        output.append('\t'.join([sub.start, sub.end, sub.content]))

output = [i+'\n' for i in output]
with open(sys.argv[1][:-3] + 'word.txt', 'w') as f:
    f.writelines(output)
