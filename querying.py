import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize Spotify API credentials

CLIENT_ID = '8c8b8ce59d5d4a6f8a4523c4b8914e55'
CLIENT_SECRET = '97d7cb45f17743d2a20ba1be4b521ace'

URI = 'http://localhost:3000'

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Initialize Spotipy with Client Credentials Flow
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

query = ['angry', 'happiness', 'satisfaction']  # Example query related to mental health podcasts
query = ' '.join(query)
print(query)
# Search for podcasts on Spotify
results = sp.search(q=query, type='episode', market = 'US', limit = 3)

results = results['episodes']['items']

for podcast in results:
    print(f"Title: {podcast['name']}")
    print(f"Description: {podcast['description']}")
    print(f"Listen here: {podcast['external_urls']['spotify']}")
    print()