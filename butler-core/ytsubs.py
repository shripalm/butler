from speakerMan import sayTheThing
from youtube_transcript_api import YouTubeTranscriptApi

def ytsubscaller():
    subs = ''
    for val in YouTubeTranscriptApi.get_transcript(sayTheThing("Enter your link postfix", True), languages=['en', 'en-US', 'en-GB', 'hi']):
        subs += val['text'] + ' '
    print(subs)
    return 'ytsubscaller'
