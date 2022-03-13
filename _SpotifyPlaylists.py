import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import urllib.request
import urllib
import subprocess
import time

#0. Useful fonctions

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

# 1. Import spotify playlist

# 1.1 Set environment variables for pass

os.environ["SPOTIPY_CLIENT_ID"]="client_id"
os.environ["SPOTIPY_CLIENT_SECRET"]="client_secret"
os.environ["SPOTIPY_REDIRECT_URI"]="http://localhost:8888/callback"

# 1.2 Get the playlist

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

i=0
max=3
list=[]
space="+"

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    i=i+1
    track = item['track']
    list.append(track['artists'][0]['name'].replace(' ','+')+space+track['name'].replace(' ','+'))
    if(i==max):
        break

# 2. Search youtube + Add Video to download

for i in range(len(list)):
    query=list[i]
    url0="https://www.youtube.com/results?search_query="+query
    fp = urllib.request.Request(url0,headers={'User-Agent': 'Chrome'})
    ab = urllib.request.urlopen(fp)
    html_page = ab.read()
    mystr = html_page.decode("utf8")
    index_num=[i for i in range(len(mystr)) if mystr.startswith('watch?', i)]
    z=mystr[index_num[0]:index_num[0]+40]
    start = 'watch? '
    end = 'webPageType'
    num_pages=z[z.find(start)+len(start):z.rfind(end)-3]
    copy2clip("https://www.youtube.com/watch?"+num_pages)
    time.sleep(1)
