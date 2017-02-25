# download list of episodes after some date

from subprocess import call
import requests
from transliterate import translit
from pytube import YouTube

def get_title(item, sub):
    raw_title = sub.name + '|' + item['snippet']['title'].replace(' ', '_')
    title = raw_title
    try:
        title = translit(raw_title, reversed=True)
    except:
        pass
    return title

def download_video(item, sub, title):
    id = item['id']['videoId']    
    link = 'http://www.youtube.com/watch?v={link}'.format(link=id)
    yt = YouTube(link)
    yt.get_videos()
    video_filename = 'videos/{title}.mp4'.format(title=title)
    yt.filter('mp4')[0].download(video_filename)
    return video_filename

def convert_video_audio(title, video_filename):
    audio_filename = 'audios/{title}.mp3'.format(title=title)
    call([
        'ffmpeg',
        '-i',
        video_filename,
        '-b:a',
        '192k',
        '-vn',
        audio_filename
    ])
    return audio_filename

def processVideos(sub, key):
    videos = loadVideos(sub, key)
    for item in videos:
        title = get_title(item, sub)
        video_filename = download_video(item, sub, title)
        audio_filename = convert_video_audio(title=title, video_filename=video_filename)

def loadVideos(sub, key):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'publishedAfter': sub.fetchedBefore,
        'channelId': sub.channel,
        'maxResults': 10,
        'order': 'date',
        'type': 'video',
        'part': 'id,snippet',
        'key': key
    }
    res = requests.get(url, params=params)
    json = res.json()

    return json['items']

