from pydantic import BaseSettings, Field
from typing import Dict, List


class Settings(BaseSettings):
    START_DATE: str = Field("2023-01-01", env="START_DATE")

    YOUTUBE_CHANNELS: Dict[str, str] = {
        "CNN": "UCupvZG-5ko_eiXAupbDfxWw",
        "MSNBC": "UCaXkIU1QidjPwiAYu6GcHjg",
        "Bloomberg Television": "UCIALMKvObZNtJ6AmdCLP7Lg",
        "NBC": "UCccjdJEay2hpb5scz61zY6Q",
        "CNBC": "UCvJJ_dzjViJCoLf5uKUTwoA",
        "Bloomberg Originals": "UCUMZ7gohGI9HcU9VNsr2FJQ",
        "NBC News": "UCeY0bbntWzzVIaj2z3QigXg",
        "CNBC Television": "UCrp_UI8XtuYfpiqluWLD7Lw",
        "CNBC International TV": "UCF8HUTbUwPKh2Q-KpGOCVGw",
        "Fox News": "UCXIJgqnII2ZOINSWNOGFThA",
        "ABC News": "UCBi2mrWuNuyYy4gbM6fU18Q",
        "Yahoo Finance 1": "UCEAZeUIeJs0IjQiqTCdVSIg",
        "Yahoo Finance 2": "UC0kuWfYTcAgKW2p36W7bpnw",
        "CNBC Make It": "UCH5_L3ytGbBziX0CLuYdQ1Q",
        "Bloomberg Technology": "UCrM7B7SL_g1edFOnmj-SDKg",
        "NBC Digital News": "UCvQbrQHNdcofvya0aG7jEjA",
        "ABC News In-depth": "UCxcrzzhQDj5zKJbXfIscCtg",
        "Cheddar": "UC04KsGq3npibMCE9Td3mVDg",
    }

    YOUTUBE_API_KEY: str = Field("", env="YOUTUBE_API_KEY")
    YOUTUBE_API_ROOT: str = Field(..., env="YOUTUBE_API_ROOT")

    YOUTUBE_ACTIVITY_COLUMNS: List = [
        "id.kind",
        "id.videoId",
        "snippet.publishedAt",
        "snippet.channelId",
        "snippet.title",
    ]

    ALPHA_VANTAGE_ROOT: str = Field(..., env="ALPHA_VANTAGE_ROOT")
    ALPHA_VANTAGE_API_KEY: str = Field(..., env="ALPHA_VANTAGE_API_KEY")
    ALPHA_VANTAGE_SYMBOLS: Dict[str, str] = {
        "Microsoft": "MSFT",
        "Apple": "AAPL",
        "Meta": "META",
        "Netflix": "NFLX",
    }


settings = Settings()
