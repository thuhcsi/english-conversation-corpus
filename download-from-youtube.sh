for url in $(cat urls.txt)
do
	youtube-dl -f 'bestvideo+bestaudio,bestaudio' --merge-output-format mkv --write-auto-sub $url
done
