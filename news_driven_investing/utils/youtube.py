import requests
import dateutil
from typing import Union
from urllib.parse import urljoin
import datetime
from youtube_transcript_api import (
    YouTubeTranscriptApi, 
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound
)

from news_driven_investing.config.settings import settings


def date_to_rfc3339(date: Union[datetime.date, datetime.datetime, str]):
    """
    Infer date type and convert to RFC 3339, which is required as input
    format for the datetime-like fields associated with the youtube Api.
    """
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
        
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def request_activities_for_channel(
    channel_id: str,
    published_after: Union[datetime.date, datetime.datetime, str], 
    published_before: Union[datetime.date, datetime.datetime, str],
    page_token: str = None,
    **params
) -> requests.Response:
    """
    For specific channel_id and time window, request all activities.
    """
    url = urljoin(settings.YOUTUBE_API_ROOT, "search")

    published_after = date_to_rfc3339(published_after)
    published_before = date_to_rfc3339(published_before)

    params.update(
        {
            "part": params.get("part", "snippet"),
            "maxResults": params.get("maxResults", 50),
            "channelId": channel_id,
            "publishedAfter": published_after,
            "publishedBefore": published_before
        }
    )

    if page_token is not None:
        params["page_token"] = page_token

    if settings.YOUTUBE_API_KEY:
        params["key"] = settings.YOUTUBE_API_KEY

    return requests.get(url, params=params)


def transcript(video_id: str) -> Union[str, None]:
    """
    Using youtube transcript api, provide transcription if available.
    """

    if video_id is None:
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(map(lambda x: x["text"], transcript))
    except Exception as e:
        return f"Exception >> {e.__class__.__name__}: {e}"
