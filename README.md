# NetflixHDR

NetflixHDR is a python script to help find netflix HD movies that don't suck.

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