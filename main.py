import requests
import os
import datetime
from pprint import pprint

def get_events(lat, long, rad, eventcode="LIVE", start_date=datetime.datetime.now(), stop_date=datetime.datetime.now()+datetime.timedelta(days=10), description=1, limit=100):
    r = requests.get("https://www.skiddle.com/api/v1/events/search/",
                    params={
                        "api_key": os.environ['SKIDDLE_API'],
                        "latitude": lat,
                        "longitude": long,
                        "radius": rad,
                        "eventcode": eventcode,
                        "order": "trending",
                        "description": 1,
                        "limit": 100,
                        "ticketsavailable": True,
                        "minDate": start_date.strftime("%Y-%m-%d"),
                        "maxDate": stop_date.strftime("%Y-%m-%d")
                    })
    r = r.json()
    artists = []
    if not r["error"]:
        for result in r["results"]:
            for artist in result["artists"]:
                if artist["spotifyartisturl"]:
                    artists.append(artist["spotifyartisturl"])
        return artists
    return None



events = get_events(53.4839, -2.2445, 10, "LIVE", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=10))
if events:
    pprint(events)
else:
    raise Exception("No gigs found")