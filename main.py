import requests
import os
import datetime
from pprint import pprint
import spotipy
import spotipy.util as util
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

print(" ".join(cfg['scope']))

def get_events(lat, long, rad, eventcode="LIVE", start_date=datetime.datetime.now(), stop_date=datetime.datetime.now()+datetime.timedelta(days=10), description=1, limit=100):
    r = requests.get("https://www.skiddle.com/api/v1/events/search/",
                    params={
                        "api_key": os.environ['SKIDDLE_API'],
                        "latitude": lat,
                        "longitude": long,
                        "radius": rad,
                        "eventcode": eventcode,
                        "order": "trending",
                        "description": description,
                        "limit": limit,
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



events = get_events(cfg['location']['lat'],
                    cfg['location']['long'],
                    cfg['location']['radius'],
                    "LIVE",
                    datetime.datetime.now(),
                    datetime.datetime.now() + datetime.timedelta(days=100))

events += get_events(cfg['location']['lat'],
                    cfg['location']['long'],
                    cfg['location']['radius'],
                    "FEST",
                    datetime.datetime.now(),
                    datetime.datetime.now() + datetime.timedelta(days=100))

to_add = []
spotify = spotipy.Spotify(auth=util.prompt_for_user_token(cfg['username'],
                                                          " ".join(cfg['scope'])))

playlist = spotify.user_playlist(cfg['username'],
                                 cfg['playlist'])
uris = []
for track in playlist["tracks"]["items"]:
    uris.append(track["track"]["uri"])

spotify.user_playlist_remove_all_occurrences_of_tracks(cfg['username'],
                                                       cfg['playlist'],
                                                       uris)
if events:
    for event in events:
        result = spotify.artist(event)
        print(result["name"])
        response = spotify.artist_top_tracks(event)
        # pprint(response['tracks'])
        for track in response['tracks'][:3]:
            print("- ", track['name'])
            to_add.append(track['uri'])
        spotify.user_playlist_add_tracks(cfg['username'],
                                         cfg['playlist'],
                                         to_add)
        to_add = []

else:
    raise Exception("No gigs found")