import pandas
import datetime
import dateutil
from typing import List, Dict

from dagster import asset
from dagster import get_dagster_logger
from dagster import (
    StaticPartitionsDefinition,
    WeeklyPartitionsDefinition,
    MultiPartitionsDefinition
)

from news_driven_investing.config.settings import settings
from news_driven_investing.utils import youtube


DATE_AND_CHANNEL_PARTITION = MultiPartitionsDefinition(
        {
            "date":  WeeklyPartitionsDefinition(
                start_date=settings.START_DATE
             ),
            "channel": StaticPartitionsDefinition(
                list(settings.YOUTUBE_CHANNELS)
            )
        }
    )


@asset(
    partitions_def=DATE_AND_CHANNEL_PARTITION,
    group_name="youtube_collect"
)
def channel_activities(context) -> List[Dict]:
    """
    For the given channelIds and weekly time partitions extract all videos.
    """

    keys = context.partition_key.keys_by_dimension

    logger = get_dagster_logger()

    date_min = dateutil.parser.parse(keys["date"])
    date_max = date_min + datetime.timedelta(days=7, seconds=-1)

    response_json = {"next_page_token": None}
    items = []

    while "next_page_token" in response_json:

        channel_id = settings.YOUTUBE_CHANNELS[keys["channel"]]

        response = youtube.request_activities_for_channel(
            channel_id=channel_id,
            published_after=date_min,
            published_before=date_max,
            page_token=response_json["next_page_token"]
        )

        msg = f"Status Code is {response.status_code}\n"
        try:
            msg += f"Json content:\n{str(response.json())[:100]}..."
        except:
            pass

        if response.status_code == 200:
            logger.info(f"Requesting activities successful!\n{msg}")
        
        else:
            error_msg = f"Requesting activities failed!\n{msg}" 
            logger.error(error_msg)

        response_json = response.json()
        items += response_json["items"]

    return items


@asset(
    partitions_def=DATE_AND_CHANNEL_PARTITION,
    group_name="youtube_collect",
    io_manager_key="pandas_io_manager"
)
def video_properties_dataframe(
        channel_activities: List[Dict]
) -> pandas.DataFrame:
    """
    Extract videos and related properties from channel_activities.
    """

    result = pandas.json_normalize(
        channel_activities
    )

    # Sometimes there are no videos available
    if not len(result):
        return pandas.DataFrame(
            dict.fromkeys(settings.YOUTUBE_ACTIVITY_COLUMNS, [])
        )
    else:
        return result[settings.YOUTUBE_ACTIVITY_COLUMNS]


@asset(
    partitions_def=DATE_AND_CHANNEL_PARTITION,
    group_name="youtube_collect",
    io_manager_key="pandas_io_manager"
)
def video_transcript(
    video_properties_dataframe
) -> pandas.DataFrame:
    """
    Extract transcript from videos, if available.
    """
    
    video_properties_dataframe["transcript"] = (
        video_properties_dataframe["id.videoId"].apply(youtube.transcript)
    )

    return video_properties_dataframe
