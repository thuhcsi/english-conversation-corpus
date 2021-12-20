#!/bin/bash
set -e
mkdir -p data
for url in $(cat urls.txt)
do
	echo $url
	(
		cd data
		#youtube-dl -f 'bestvideo+bestaudio,bestaudio' $url
		youtube-dl -f 'bestaudio' $url
	)
done

mv 'data/English conversation 80-8_c0YgLOcdo.m4a' 'data/English Conversation 80-8_c0YgLOcdo.m4a'

for i in data/*.webm
do
	ffmpeg -i $i -ac 1 -ar 16000 ${i%webm}wav
done

for i in data/*.m4a
do
	ffmpeg -i $i -ac 1 -ar 16000 ${i%m4a}wav
done
