"""
Looking for HD movies that don't suck? This might help.

Read the list of movies from https://hd-report.com/list-of-4k-ultra-hd-movies-tv-shows-on-netflix/
and grab the ratings from the Open Movie Database and merge the two together

You'll need to create a .env file with:
OMDBAPI_KEY=<your omdb api key>

Code by: wlm2048@gmail.com
"""
import os
import time

import requests
from tqdm import tqdm
from filecache import filecache
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def main():
    """
    Grab the movies and look up the details
    """
    load_dotenv()
    apikey = os.getenv('OMDBAPI_KEY')
    k, movies = hashify()
    # k = ['Title', '4k', 'HDR', 'Audio', 'Type', 'New']
    for movie in tqdm(movies):
        details = fetch_details(apikey, movie['Title'])
        if 'Ratings' in details:
            for rating in details['Ratings']:
                if not rating['Source'] in k:
                    k.append(rating['Source'])
                movie[rating['Source']] = rating['Value']
            movie['Average Rating'] = get_average(details['Ratings'])


def hashify():
    """
    Turn the HTML into a dict
    """
    movies = []
    movies_html = fetch_movies()
    soup = BeautifulSoup(movies_html, 'html.parser')
    movies_table = soup.find('table', class_='tablesorter')
    keys = [x.find('span').text for x in movies_table.find_all('th')]
    rows = movies_table.find_all('tr')
    for row in rows[1:]:
        values = [x.text for x in row.find_all('td')]
        movies.append(dict(zip(keys, values)))
    return keys, movies


def get_average(rating):
    """
    Generate an average rating
    :param rating:
    :return average:
    """
    num_ratings = len(rating)
    total = 0
    for rat in [x['Value'] for x in rating]:
        if '/' in rat:
            a = [float(b) for b in rat.split('/')]
            total = total + round(a[0] / a[1], 2)
        if '%' in rat:
            total = total + round(float(rat.replace('%', '')) / 100, 2)
    return round(total / num_ratings, 2)


@filecache(24 * 60 * 60)
def fetch_movies():
    r = requests.get('https://hd-report.com/list-of-4k-ultra-hd-movies-tv-shows-on-netflix/')
    return r.text


@filecache(25 * 60 * 60)
def fetch_details(apikey, title):
    time.sleep(0.5)
    try:
        r = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={apikey}")
    except ConnectionResetError:
        print(f"Connection reset on {title}")
        return
    return r.json()


if __name__ == '__main__':
    main()
