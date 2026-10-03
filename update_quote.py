import os
import requests
from bs4 import BeautifulSoup
import random
import re

username = "wasilll"
tmdb_key = os.environ.get("TMDB_API_KEY")

# Disguise the scraper as a standard Chrome web browser to bypass bot protection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://letterboxd.com/'
}

# Extract 5/5 movies from Letterboxd
res = requests.get(f"https://letterboxd.com/{username}/films/rated/5/", headers=headers)

if res.status_code != 200:
    print(f"Error: Letterboxd returned HTTP {res.status_code}")
    exit(1)

soup = BeautifulSoup(res.text, 'html.parser')
movies = [img.get('alt') for img in soup.select('.film-poster img') if img.get('alt')]

if not movies:
    print("No movies found. Check username or Letterboxd structure.")
    exit(1)

selected_movie = random.choice(movies)
quote = "Absolute cinema." # Fallback quote if TMDB has no tagline

# Fetch tagline from TMDB
search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_key}&query={selected_movie}"
search_res = requests.get(search_url).json()

if search_res.get('results'):
    movie_id = search_res['results'][0]['id']
    details_res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_key}").json()
    if details_res.get('tagline'):
        quote = details_res['tagline']

formatted_quote = f'<i>"{quote}" — {selected_movie}</i>'

# Load and update README
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# Replace content between markers
readme = re.sub(
    r'<!-- quote-start -->.*?<!-- quote-end -->', 
    f'<!-- quote-start -->\n  {formatted_quote}\n  <!-- quote-end -->', 
    readme, 
    flags=re.DOTALL
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
