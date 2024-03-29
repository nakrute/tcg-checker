"""
This was done as a prefect example, but without a way to kickoff a the remote worker pool
I found this not the best way to run the bot. For now using GHA, and staging the bot
a few minutes early so that it's waiting for the proper time to run.
"""

import requests as re
import json
import datetime as dt
from prefect import flow
from discord import SyncWebhook

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


@flow(log_prints=True)
def tcg_checker():
    print("Generating class for store: Mitsuwa")
    mitsuwa = StoreDetails(organizer_id=5567,
                           limit=50,
                           offset=0,
                           game_title_id=4,
                           application_open_flg=0,
                           country_code="US")
    print("Generating class for store: Waypoint")
    waypoint = StoreDetails(organizer_id=464,
                            limit=50,
                            offset=0,
                            game_title_id=4,
                            application_open_flg=0,
                            country_code="US")

    print("Getting event list for store: Mitsuwa")
    mitsuwa.get_current_events()
    mitsuwa.first_and_last_event()
    print("Getting event list for store: Waypoint")
    waypoint.get_current_events()
    waypoint.first_and_last_event()

    print("Running Webhook")
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    webhook.send(f"Number of events at Mitsuwa right now: {len(mitsuwa._events)}\n"
                 f"First Event Date for Mitsuwa is: {mitsuwa.first_event_date}\n"
                 f"Last Event Date for Mitsuwa is: {mitsuwa.last_event_date}")
    webhook.send(f"Number of events at Waypoint right now: {len(waypoint._events)}\n"
                 f"First Event Date for Waypoint is: {waypoint.first_event_date}\n"
                 f"Last Event Date for Waypoint is: {waypoint.last_event_date}")
    print("Done")


if __name__ == "__main__":
    tcg_checker.serve(name="my-discord-bot",
                      tags=["tcg-checker", "automation"],
                      parameters={},
                      interval=60)
