"""
Looking for HD movies that don't suck? This might help.

Read the list of movies from https://hd-report.com/list-of-4k-ultra-hd-movies-tv-shows-on-netflix/
and grab the ratings from the Open Movie Database and merge the two together

You'll need to create a .env file with:
OMDBAPI_KEY=<your omdb api key>

Code by: wlm2048@gmail.com
"""
import os

import pandas
import requests
from tqdm import tqdm
from filecache import filecache
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def main():
    """
    Grab the movies and look up the details
    """
    load_dotenv()
    apikey = os.getenv('OMDBAPI_KEY')
    column_keys, movies = hashify()
    # k = ['Title', '4k', 'HDR', 'Audio', 'Type', 'New']
    column_keys.append('Average Rating')
    pbar = tqdm(movies)
    for movie in pbar:
        pbar.set_description(movie['Title'])
        details = fetch_details(apikey, movie['Title'])
        if 'Ratings' in details and len(details['Ratings']) > 0:
            for rating in details['Ratings']:
                if not rating['Source'] in column_keys:
                    column_keys.append(rating['Source'])
                movie[rating['Source']] = rating['Value']
            movie['Average Rating'] = get_average(details['Ratings'])

    m2d = [[movie[c_key] if c_key in movie else 'NA' for c_key in column_keys] for movie in movies]
    moviesDF = pandas.DataFrame(columns=column_keys, data=m2d)
    moviesDF.to_csv('netflixhdr.csv', index=False)


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
    try:
        r = session.get(f"http://www.omdbapi.com/?t={title}&apikey={apikey}")
    except requests.exceptions.ConnectionError:
        print(f"Connection reset on {title}")
        return
    return r.json()


if __name__ == '__main__':
    main()
