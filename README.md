# Youtube-grabber

[![Build Status](https://travis-ci.org/Bloomca/youtube-mp3-grabber.svg?branch=master)](https://travis-ci.org/Bloomca/youtube-mp3-grabber)

This is a simple CLI application which allows to subscribe to channels in youtube, and then you'll be able to download all new episodes (s), both as a video and an audio. I use it for automatic downloading audios, to be able to listen it as a podcast later. 
All subscriptions and latest timestamps are stored in sqlite, so episodes shouldn't be downloaded twice.

## Starting locally

If you want to start it locally, you have to have next things:
```shell
pip
sqlite3 # for storing subscriptions and timestamps
ffmpeg # for converting video to mp3
```

To actually use the application, do the following steps:
```shell
mkdir audios videos # for placing files
# activate virtualenv
pip install -r requirements.txt
python src/db.py # to set up sqlite db
python 
```

## Usage

It is a CLI app built with [click](http://click.pocoo.org/5/), so the help is available via the command:
```shell
python src/application.py --help
```

Basically, where are few flags and commands.
Flags:
- channel -- channel id to subscribe/unsubscribe
- name -- name for the channel (all files will be prefixed with it)
- key -- Youtube API key. It is annoying, but I can't compromise mine, sorry

Commands:
- subscribe -- subscribe to the given channel, saving given name. It will subscribe and set timestamp to current momemnt, so only episoded which were published after will be downloaded
- show -- show all active subscriptions, with the date of the last fetching
- update -- actual fetching of all new episodes. It will download everything, convert video to mp3 and place to the corresponding folders, and after this update the timestamp.

## License

MIT License

Copyright (c) 2017 Vsevolod Zaikov

