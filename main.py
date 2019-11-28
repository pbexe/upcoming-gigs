import requests
import os

r = requests.get("https://www.skiddle.com/api/v1/events/search/",
                 params={
                     "api_key": os.environ['SKIDDLE_API'],
                     "latitude": 53.4839,
                     "longitude": -2.2445,
                     "radius": 5,
                     "eventcode": "LIVE",
                     "order": "trending",
                     "description": 1,
                     "limit": 100,
                     "ticketsavailable": True,
                 })

print(r.text)