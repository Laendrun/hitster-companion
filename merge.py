import os
import pandas as pd
import json

# Load the CSV file
playlist = pd.read_csv('./assets/playlist_hitster_100%_francais.csv')

# Extract the Spotify Track ID from the Track URI column
playlist['Spotify Track ID'] = playlist['Track URI'].str.replace('spotify:track:', '')
# print("Columns in playlist DataFrame:", playlist.columns)
print(playlist)

with open('./assets/gameset_database.json', 'r', encoding='utf-8') as f:
  gameset_csv = json.load(f)

target_sku = 'aaaa0010' # Tubes 100% Français
gamesets = gameset_csv['gamesets']

result = next(
  (item for item in gamesets if item['sku'] == target_sku),
  None
)['gameset_data']

cards_df = pd.DataFrame(result['cards'])
gameset = cards_df.rename(columns={'Spotify': 'Spotify Track ID'})

print(gameset)

merged = pd.merge(
  gameset,
  playlist,
  on='Spotify Track ID',
  how='left'
)

filtered = merged[['CardNumber', 'Spotify Track ID', 'Track Name', 'Artist Name(s)', 'Release Date']]
filtered = filtered.rename(columns={
  'Spotify Track ID': 'spotify_id',
  'Track Name': 'name',
  'Artist Name(s)': 'artist',
  'Release Date': 'year'
})
filtered['year'] = filtered['year'].str[:4]

filtered['spotify_url'] = 'https://open.spotify.com/track/' + filtered['spotify_id']
filtered['ytm_id'] = ''
filtered['ytm_url'] = 'https://music.youtube.com/watch?v='

filtered_dict = filtered.to_dict(orient='records')
with open(f"{result['gameset_name']}.json", 'w', encoding='utf-8') as f:
  json.dump(filtered_dict, f, indent=2, ensure_ascii=False)

# filtered.to_json(f"{result['gameset_name']}.json", orient='records', indent=2, force_ascii=False)

