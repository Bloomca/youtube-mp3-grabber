from subprocess import call
import requests
from transliterate import translit
from pytube import YouTube

def get_title(item, sub):
    """
    Get title of the youtube video
    Try to transliterate it, in case it is
    in non-cyrillic characters
    """
    raw_title = (sub.name + '|' + item['snippet']['title']).replace(' ', '_')
    title = raw_title
    try:
        title = translit(raw_title, reversed=True)
    except:
        pass
    return title

def download_video(item, title):
    """
    Download video from youtube in mp4 format
    """
    video_id = item['id']['videoId']
    link = 'http://www.youtube.com/watch?v={link}'.format(link=video_id)
    yt_files = YouTube(link)
    yt_files.get_videos()
    video_filename = 'videos/{title}.mp4'.format(title=title)
    yt_files.filter('mp4')[0].download(video_filename)
    return video_filename

def convert_video_audio(title, video_filename):
    """
    Convert given video to the mp3
    """
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

def process_videos(sub, key):
    """
    get all new episodes for the given subscription
    download them and convert to the mp3
    """
    videos = load_videos(sub, key)
    for item in videos:
        title = get_title(item, sub)
        video_filename = download_video(item, title)
        convert_video_audio(title=title, video_filename=video_filename)

def load_videos(sub, key):
    """
    fetch all new episodes of the youtube channel
    """
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

