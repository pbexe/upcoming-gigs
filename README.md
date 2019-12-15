# Upcoming Gigs

> Populates a spotify plalist with upcoming gigs in a region

## To run

Install requirements
```sh
pip install -r requirements.txt
```

Set environment variables:
```sh
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
export SKIDDLE_API='your-skiddle-api-key'
```

Update the config file:
```yaml
username: Your Username
playlist: URI of the playlist you want to use
scope:
  - playlist-modify-public
location:
  lat: The latitude of the target
  long: The longitude of the target
  radius: The search radius
```

Run
```sh
python main.py
```