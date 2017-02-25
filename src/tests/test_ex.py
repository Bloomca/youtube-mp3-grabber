
# Third-party imports...
from src.youtube import get_title
from src.db import Subscription
from nose.tools import assert_true

def create_yt_video():
    return {'snippet': {'title': 'some title'} }

def test_request_response():
    sub = Subscription(channel='some', name='Some channel name', fetchedBefore='dummy')
    video = create_yt_video()
    title = get_title(video, sub)

    # Check there are no spaces here.
    assert_true(' ' not in title)
