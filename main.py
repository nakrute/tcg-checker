import requests as re
import json
import datetime as dt
from typing import Any
import discord
from dotenv import load_dotenv
from discord.ext import tasks

API_URL = "https://api.bandai-tcg-plus.com/api/user/event/list"
TOKEN = <TOKEN>

load_dotenv()
client = discord.Client(intents=discord.Intents.default())


class StoreDetails:
    def __init__(self,
                 organizer_id: int,
                 limit: int,
                 offset: int,
                 game_title_id: int,
                 application_open_flg: int,
                 country_code: str) -> None:
        self.api_url = API_URL
        self.organizer_id = organizer_id
        self.limit = limit
        self.offset = offset
        self.game_title_id = game_title_id
        self.application_open_flg = application_open_flg
        self.country_code = country_code
        self.start_date = dt.datetime.today().strftime("%Y-%m-%d")

    def get_current_events(self) -> dict[str, Any]:
        data = re.get(url=f"{self.api_url}?"
                          f"organizer_id={self.organizer_id}&"
                          f"limit={self.limit}&offset={self.offset}&"
                          f"game_title_id={self.game_title_id}&"
                          f"application_open_flg={self.application_open_flg}&"
                          f"country_code[]={self.country_code}"
                          f"&start_date={self.start_date}")
        json_data = json.loads(data.text)["success"]["event_list"]
        return json_data


mitsuwa = StoreDetails(organizer_id=5567,
                       limit=50,
                       offset=0,
                       game_title_id=4,
                       application_open_flg=0,
                       country_code="US",)
waypoint = StoreDetails(organizer_id=464,
                        limit=50,
                        offset=0,
                        game_title_id=4,
                        application_open_flg=0,
                        country_code="US",)


@tasks.loop(hours=1.0)
async def check_shops():
    channel = client.get_channel(1191833508344242176)
    await channel.send(f"Number of events at Mitsuwa right now: {len(mitsuwa.get_current_events())}")
    await channel.send(f"Number of events at Waypoint right now: {len(waypoint.get_current_events())}")


@client.event
async def on_ready():
    check_shops.start()

client.run(TOKEN)
