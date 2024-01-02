# SpotifyPlayground
scripts and other code for interacting with the Spotify Web API.

For more on using the Spotify Web API and for generating your credentials, [go here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started).

## SpotifyPlaylistExporter
Can't remember if you've used a track in a playlist before? Can't remember what playlist you put that track on?

`SpotifyPlaylistExplorer` will take a list of public Spotify Playlist URIs (`playlists.txt`) and return the ordered tracklisting from those playlists.

If you are having trouble finding the playlist URI, [try this link](https://community.spotify.com/t5/Spotify-for-Developers/Get-Playlist-URI-with-updated-Desktop-Look/td-p/5185605).

### Usage
**tl;dr**: `python processPlaylists.py`

To execute this you will need:
- a `config.json` that looks like:
```
{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}
```
- a `playlists.txt` that looks like:
```
spotify:playlist:6PddocD482We229sj3xoIl
spotify:playlist:0jdLcnwfqplEFvhRLL4KH0
```
(etc.)

![image](https://github.com/mrogove/SpotifyPlayground/assets/7624639/0d9a3a65-b210-4ded-9ed1-5ba9e296afcc)

You can optionally specify a delimiter if the default (`;;;`) doesn't work for you:

`python processPlaylists.py --delimiter "@|@"`
