English conversation corpus
----

## Introduction

This corpus collects 66 publicly available videos from the [English Conversation channel on YouTube](https://www.youtube.com/@AnhNguVIPS).

## Annotation

The annotations are located in the `conversations` directory.

Please note that the speaker labels are only shared in that video, not shared among all videos.

## Usage

### Download the audios and videos

Please use `download-audio.sh` and `download-video.sh` to download the audios and videos.

### Segment the audios

Please run `segment.py` to segment the audios into utterances. You will see some warnings, but they are fine.

```sh
python segment.py
```

## Citation

Please cite [our paper on ICASSP 2022](https://ieeexplore.ieee.org/abstract/document/9747837/) to refer to this corpus.

```bibtex
@inproceedings{li_enhancing_2022,
	title = {Enhancing {Speaking} {Styles} in {Conversational} {Text}-to-{Speech} {Synthesis} with {Graph}-{Based} {Multi}-{Modal} {Context} {Modeling}},
	copyright = {All rights reserved},
	doi = {10.1109/ICASSP43922.2022.9747837},
	booktitle = {{ICASSP} 2022 - 2022 {IEEE} {International} {Conference} on {Acoustics}, {Speech} and {Signal} {Processing} ({ICASSP})},
	author = {Li, Jingbei and Meng, Yi and Li, Chenyi and Wu, Zhiyong and Meng, Helen and Weng, Chao and Su, Dan},
	year = {2022},
	note = {ISSN: 2379-190X},
	keywords = {Speech, Recurrent neural networks, Acoustics, Conferences, Data mining, Signal processing, Speech enhancement, speaking style, conversational text-to-speech synthesis, graph neural network},
	pages = {7917--7921},
}
```

## Copyright

We have the copyrights of the annotations and scripts and they are licensed under [GPLv3](https://github.com/thuhcsi/english-conversation-corpus/blob/master/LICENSE).

We do not have the copyrights of the audios and videos in this corpus. They belong to the [English Conversation channel on YouTube](https://www.youtube.com/@AnhNguVIPS).

Please only use the corpus for non-commercial research and/or educational purposes.
