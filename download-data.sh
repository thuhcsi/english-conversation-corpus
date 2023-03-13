#!/bin/bash
set -e

# Download audios (1.9G)
curl -L "https://cloud.tsinghua.edu.cn/f/aae5883114e94b9584d4/?dl=1" | tar xvf -

# Process audios
mv 'data/English conversation 80-8_c0YgLOcdo.m4a' 'data/English Conversation 80-8_c0YgLOcdo.m4a'

for i in data/*.webm
do
	ffmpeg -i "$i" -ac 1 -ar 16000 "${i%webm}wav"
done

for i in data/*.m4a
do
	ffmpeg -i "$i" -ac 1 -ar 16000 "${i%m4a}wav"
done

# Download videos (22G)
curl -L \
	"https://cloud.tsinghua.edu.cn/f/369932b575bc40009719/?dl=1" \
	"https://cloud.tsinghua.edu.cn/f/51651e1fbe52498a87e5/?dl=1" \
	"https://cloud.tsinghua.edu.cn/f/53fec002a4464a809f43/?dl=1" \
	"https://cloud.tsinghua.edu.cn/f/aef333b32bfb433fa1e6/?dl=1" \
	"https://cloud.tsinghua.edu.cn/f/e36923e117c84d5fafd5/?dl=1" | tar xvf -

# Process videos
mv 'data/English conversation 80-8_c0YgLOcdo.mkv' 'data/English Conversation 80-8_c0YgLOcdo.mkv'
