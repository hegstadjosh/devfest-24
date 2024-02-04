import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ai_implementation

# Initialize Spotify API credentials

CLIENT_ID = '8c8b8ce59d5d4a6f8a4523c4b8914e55'
CLIENT_SECRET = '97d7cb45f17743d2a20ba1be4b521ace'

URI = 'http://localhost:3000'

sentiments = ai_implementation.runJournal()
print(sentiments)

# Initialize Spotipy with Client Credentials Flow
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

if sentiments:
    first3 = list(sentiments.keys())[-3:]
    last3 =  list(sentiments.keys())[:3]
    
    def getQuery(query):
        query = ' '.join(query)
        print('')
        # Search for podcasts on Spotify
        results = sp.search(q=query, type='episode', market = 'US', limit = 3)
        
        results = results['episodes']['items']
        
        for podcast in results:
            print(f"Title: {podcast['name']}")
            print(f"Description: {podcast['description']}")
            print(f"Listen here: {podcast['external_urls']['spotify']}")
            print()
    
    print("\n Podcasts recommended based on your feelings now")
    getQuery(first3)
    print("You might also like: ")
    getQuery(last3)
