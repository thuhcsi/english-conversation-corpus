import subprocess
import traceback
from pathlib import Path
from multiprocessing import Pool

path = Path('.')
data = path / 'data'
conversations = path / 'conversations'
segmented = path / 'segmented'
segmented.mkdir(exist_ok=True)

def convert_time(time):
    time = list(map(float, time.split(':')))
    return time[0] * 3600 + time[1] * 60 + time[2]

def clip_wav(source, start, end, target):
    duration = '%.6f' % (end - start)
    start = '%.6f' % start
    subprocess.run(['ffmpeg', '-i', source, '-ss', start, '-t', duration, '-c', 'copy', target, '-v', 'quiet', '-y'])

def process(filename):
    i = filename[21:23]
    wav = data / (filename[:-3] + 'wav')

    file = open(conversations / filename)
    lines = file.readlines()
    file.close()

    breaks = [j for j, line in enumerate(lines) if line == '\n']
    breaks.insert(0, -1)
    if breaks[-1] != len(lines) - 1:
        breaks.append(len(lines)-1)
    segmented_conversations = [lines[breaks[j]+1:breaks[j+1]] for j in range(len(breaks)-1)]

    for j, conversation in enumerate(segmented_conversations):
        for k, line in enumerate(conversation):
            try:
                speaker, start, end, content = line.split('\t')
                start, end = convert_time(start), convert_time(end)
                if end - start <= 0:
                    print('Invalid time:', filename, line)
                    continue
                if end - start < 0.2:
                    print('Time is too short:', filename, line)
                if end - start > 15:
                    print('Time is too long:', filename, line)
                output = segmented / f'{i}-{j}-{k}-{speaker}.txt'
                with open(output, 'w') as f:
                    f.write(content)
                output = segmented / f'{i}-{j}-{k}-{speaker}.wav'
                clip_wav(wav, start, end, output)
            except:
                print(traceback.print_exc())
                print('Error when processing:', filename, line)

filenames = sorted([i.name for i in conversations.rglob('*.txt')])
with Pool() as pool:
    pool.map(process, filenames)
