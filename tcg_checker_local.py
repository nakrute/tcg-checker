import requests as re
import json
import datetime as dt
from discord import SyncWebhook
import time

API_URL = "https://api.bandai-tcg-plus.com/api/user/event/list"
WEBHOOK_URL = "https://discord.com/api/webhooks/1192839108402348182/U7kvQN32s0-O38OkBWZJUnU37PUtTcG93Iqcqs9crBsPyhYxdcPpPY40y79QHzPtoQDj"


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
        self._events = []
        self.first_event_date = ""
        self.last_event_date = ""

    def get_current_events(self) -> None:
        data = re.get(url=f"{self.api_url}?"
                          f"organizer_id={self.organizer_id}&"
                          f"limit={self.limit}&offset={self.offset}&"
                          f"game_title_id={self.game_title_id}&"
                          f"application_open_flg={self.application_open_flg}&"
                          f"country_code[]={self.country_code}"
                          f"&start_date={self.start_date}")
        json_data = json.loads(data.text)["success"]["event_list"]
        self._events = json_data

    def first_and_last_event(self) -> None:
        self.first_event_date = self._events[0]['start_datetime']
        self.last_event_date = self._events[-1]['start_datetime']

mitsuwa = StoreDetails(organizer_id=5567,
                       limit=50,
                       offset=0,
                       game_title_id=4,
                       application_open_flg=0,
                       country_code="US")
waypoint = StoreDetails(organizer_id=464,
                        limit=50,
                        offset=0,
                        game_title_id=4,
                        application_open_flg=0,
                        country_code="US")
montasy = StoreDetails(organizer_id=442 ,
                       limit=50,
                       offset=0,
                       game_title_id=4,
                       application_open_flg=0,
                       country_code="US")
b_dragon = StoreDetails(organizer_id=3266,
                        limit=50,
                        offset=0,
                        game_title_id=4,
                        application_open_flg=0,
                        country_code="US")
silk_road = StoreDetails(organizer_id=1003,
                         limit=50,
                         offset=0,
                         game_title_id=4,
                         application_open_flg=0,
                         country_code="US")
gilded_raven = StoreDetails(organizer_id=6365,
                            limit=50,
                            offset=0,
                            game_title_id=4,
                            application_open_flg=0,
                            country_code="US")

minute_check = dt.datetime.now().minute
while True:
    if 1 <= minute_check <= 5:

        run_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mitsuwa.get_current_events()
        # mitsuwa.first_and_last_event()
        waypoint.get_current_events()
        # waypoint.first_and_last_event()
        montasy.get_current_events()
        # montasy.first_and_last_event()
        b_dragon.get_current_events()
        # b_dragon.first_and_last_event()
        silk_road.get_current_events()
        # silk_road.first_and_last_event()
        gilded_raven.get_current_events()
        # gilded_raven.first_and_last_event()

        webhook = SyncWebhook.from_url(WEBHOOK_URL)
        webhook.send(f"Data collected at: {run_time}")
        webhook.send(f"Number of events at Mitsuwa right now: {len(mitsuwa._events)}\n")
        webhook.send(f"Number of events at Waypoint right now: {len(waypoint._events)}\n")
        webhook.send(f"Number of events at Montasy right now: {len(montasy._events)}\n")
        webhook.send(f"Number of events at Bearded Dragon right now: {len(b_dragon._events)}\n")
        webhook.send(f"Number of events at Silk Road right now: {len(silk_road._events)}\n")
        webhook.send(f"Number of events at Gilded Raven right now: {len(gilded_raven._events)}\n")
        break
    else:
        minute_check = dt.datetime.now().minute
        time.sleep(10)
