# TTSS

A simple Python wrapper for TTSS (Traffic Tram Supervision System) API.

## Requirements
* Python 3.8+

## Installation
```
pip install ttss
```

## Usage

For MPK Kraków trams:
```py
ttss = TTSS(base_url='http://www.ttss.krakow.pl')
```

For MPK Kraków buses:
```py
ttss = TTSS(base_url='http://ttss.mpk.krakow.pl')
```

> Note: the base URL must not contain `/internetservice` and must not end with `/`.
