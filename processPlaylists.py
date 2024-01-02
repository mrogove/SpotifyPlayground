import argparse
import requests
import csv
import json
import time

class SpotifyPlaylistExporter:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()

    def get_access_token(self):
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'client_credentials'}
        response = requests.post(url, headers=headers, data=payload, auth=(self.client_id, self.client_secret))
        return response.json()['access_token']

    def get_playlist_tracks(self, playlist_id):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        
        tracks = []
        while url:
            response = requests.get(url, headers=headers)
            data = response.json()
            tracks.extend(data['items'])
            url = data.get('next')

        return tracks

    def get_playlist_details(self, playlist_id):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data['name']

    def export_to_csv(self, playlist_uris, file_name, delimiter):
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            headers = ['Playlist Name', 'Playlist ID', 'Track URL', 'Track Name', 'Artist(s)', 'Album Name']
            
            file.write(delimiter.join(headers) + '\n')
            for uri in playlist_uris:
                playlist_id = uri.split(':')[-1]
                playlist_name = self.get_playlist_details(playlist_id)
                tracks_info = self.get_playlist_tracks(playlist_id)

                for item in tracks_info:
                    track = item['track']
                    track_url = track['external_urls']['spotify']
                    track_name = track['name']
                    artist_names = ', '.join(artist['name'] for artist in track['artists'])
                    album_name = track['album']['name']

                    row = delimiter.join([playlist_name, playlist_id, track_url, track_name, artist_names, album_name])
                    file.write(row + '\n')

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export Spotify playlists to CSV.')
    parser.add_argument('--delimiter', default=';;', help='Delimiter to use in the CSV file, default is `;;;`')
    args = parser.parse_args()

    start_time = time.time()

    with open('config.json', 'r') as file:
        config = json.load(file)

    exporter = SpotifyPlaylistExporter(config['client_id'], config['client_secret'])

    with open('playlists.txt', 'r') as file:
        playlist_uris = [line.strip() for line in file if line.strip()]

    exporter.export_to_csv(playlist_uris, 'spotify_playlist_tracks.csv', args.delimiter)

    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")
    print("CSV file has been created.")
