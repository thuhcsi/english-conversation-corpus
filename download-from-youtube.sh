#!/bin/bash
set -e
for url in $(cat urls.txt)
do
	echo $url
	youtube-dl -f 'bestvideo+bestaudio,bestaudio' --merge-output-format mkv --write-auto-sub $url
done
