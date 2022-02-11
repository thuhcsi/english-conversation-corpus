import librosa
import os
from tqdm import tqdm
from pathlib import Path
import traceback
import numpy as np

path = Path('.')
conversations = path / 'conversations'

def convert_time(time):
    time = list(map(float, time.split(':')))
    return time[0] * 3600 + time[1] * 60 + time[2]

sentence_words = []
speaker_maps = {}

sentence_durations = []
speaker_sentences = []
speaker_durations = []
speaker_cnt = 0

def process(filename):
    i = filename[21:23]
    global speaker_cnt
    #wav = data / (filename[:-3] + 'wav')
    file = open(conversations / filename)
    lines = file.readlines()
    file.close()

    breaks = [j for j, line in enumerate(lines) if line == '\n']
    breaks.insert(0, -1)
    if breaks[-1] != len(lines) - 1:
        breaks.append(len(lines)-1)
    segmented_conversations = [lines[breaks[j]+1:breaks[j+1]] for j in range(len(breaks)-1)]
    conversation_statics = []
    for j, conversation in enumerate(segmented_conversations):
        conversation_statics.append([0,[],0]) #utts, speakers, times
        for k, line in enumerate(conversation):
            try:
                speaker, start, end, content = line.split('\t')
                start, end = convert_time(start), convert_time(end)
                if end - start <= 0:
                    #print('Invalid time:', filename, line)
                    continue
                if end - start < 0.2:
                    #print('Time is too short:', filename, line)
                    pass
                if end - start > 15:
                    #print('Time is too long:', filename, line)
                    pass
                conversation_statics[j][0] = max(conversation_statics[j][0], k+1)
                
                if speaker not in conversation_statics[j][1]:
                    conversation_statics[j][1].append(speaker)
                    speaker_maps[filename+str(j)+'-'+speaker] = speaker_cnt
                    speaker_sentences.append(0)
                    speaker_durations.append(0)
                    speaker_cnt += 1
                conversation_statics[j][2] += (end-start)
                speaker_sentences[speaker_maps[filename+str(j)+'-'+speaker]] += 1
                speaker_durations[speaker_maps[filename+str(j)+'-'+speaker]] += (end-start)
                sentence_words.append(len(line.split(' ')))
                sentence_durations.append(end-start)
#                 output = segmented / f'{i}-{j}-{k}-{speaker}.txt'
#                 with open(output, 'w') as f:
#                     f.write(content)
#                 output = segmented / f'{i}-{j}-{k}-{speaker}.wav'
#                 clip_wav(wav, start, end, output)
            except:
                print(traceback.print_exc())
                print('Error when processing:', filename, line)
    #print(conversation_statics)
    return conversation_statics

video_statics = []
for filename in os.listdir(conversations):
    #print(filename)
    video_statics.append(process(filename))

# for each video:
conversation_nums = []
speaker_nums = []
durations = []
conversation_durations = []
conversation_sentences = []
conversation_speakers = []


for video in video_statics:
    #print(video)
    conversation_num = len(video)
    speaker_num = 0
    duration = 0
    for conv in video:
        conversation_durations.append(conv[2])
        conversation_sentences.append(conv[0])
        conversation_speakers.append(len(conv[1]))
        for speaker in conv[1]:
            speaker_num = max(speaker_num, ord(speaker[0].upper())-ord('A')+1)
        duration += conv[2]
    #print(conversation_num, speaker_num, duration)
    conversation_nums.append(conversation_num)
    speaker_nums.append(speaker_num)
    durations.append(duration)
    
    
    

conversation_nums.sort()
speaker_nums.sort()
durations.sort()
conversation_durations.sort()
conversation_sentences.sort()
conversation_speakers.sort()
speaker_sentences.sort()
speaker_durations.sort()
sentence_words.sort()
sentence_durations.sort()
                                     
print('For each video')
print('Number of conversations:    Minium:{} Average:{} Maxium:{}'.format(conversation_nums[0], np.array(conversation_nums).mean(), conversation_nums[-1]))
print('Number of speakers:    Minium:{} Average:{} Maxium:{}'.format(speaker_nums[0], np.array(speaker_nums).mean(), speaker_nums[-1]))
print('Duration:    Minium:{} Average:{} Maxium:{}'.format(durations[0]/60, np.array(durations).mean()/60, durations[-1]/60))

print()
print('For each conversation')
print('Number of sentences:    Minium:{} Average:{} Maxium:{}'.format(conversation_sentences[0], np.array(conversation_sentences).mean(), conversation_sentences[-1]))
print('Number of speakers:    Minium:{} Average:{} Maxium:{}'.format(conversation_speakers[0], np.array(conversation_speakers).mean(), conversation_speakers[-1]))
print('Duration:    Minium:{} Average:{} Maxium:{}'.format(conversation_durations[0], np.array(conversation_durations).mean(), conversation_durations[-1]/60))

print()
print('For each speaker')
print('Number of sentences:    Minium:{} Average:{} Maxium:{}'.format(speaker_sentences[0], np.array(speaker_sentences).mean(), speaker_sentences[-1]))
print('Duration:    Minium:{} Average:{} Maxium:{}'.format(speaker_durations[0], np.array(speaker_durations).mean(), speaker_durations[-1]/60))

print()
print('For each sentence')
print('Number of words:    Minium:{} Average:{} Maxium:{}'.format(sentence_words[0], np.array(sentence_words).mean(), sentence_words[-1]))
print('Duration:    Minium:{} Average:{} Maxium:{}'.format(sentence_durations[0], np.array(sentence_durations).mean(), sentence_durations[-1]))

