# NetflixHDR

NetflixHDR is a python script to help find netflix HD movies that don't suck.

## The Problem

hd-report.com has a list of all the HD movies [available on Netflix](https://hd-report.com/list-of-4k-ultra-hd-movies-tv-shows-on-netflix/), however they don't include the ratings for the movies. I use this as a starting point, then connect to the Open Movie Database, and pull ratings for these movies. Once merged together, we can find a movie or a show that not only looks good, but is actually entertaining to watch.

## Requirements

An [OMDB](http://www.omdbapi.com/) API key.

It caches as much as possible, so you should be able to get by with the free API key.

## Installation

Use pip or manually install the requirements in requirements.txt.

```bash
pip install -r requirements.txt
```

Add your API key to a```.env``` file with the format:
```bash
OMDBAPI_KEY=<your api key here>
```

## Usage

Run the script, it will generate netflixhdr.csv for your use.

```bash
netflixhdr.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)