# OsmToRoadGraph v.0.3

[![Build Status](https://travis-ci.org/AndGem/OsmToRoadGraph.svg?branch=master)](https://travis-ci.org/AndGem/OsmToRoadGraph)
[![codecov](https://codecov.io/gh/AndGem/OsmToRoadGraph/branch/master/graph/badge.svg)](https://codecov.io/gh/AndGem/OsmToRoadGraph)

<!-- TOC -->

- [Introduction](#introduction)
    - [Requirements](#requirements)
    - [Usage](#usage)
            - [Example](#example)
    - [Output Format](#output-format)
            - [Example](#example-1)
    - [Research](#research)

<!-- /TOC -->

# Introduction

This tools can convert [OpenStreetMap's](http://www.openstreetmap.org) OSM XML files to a simple graph format for further processing. It is compatible with Python 2 and 3. 

## Requirements
* Python 2.7+/Python 3.6+/PyPy
* [future package](https://pypi.python.org/pypi/future) / run `pip install -r requirements.txt`
* An OSM XML file

## Usage
```
Usage: run.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
  -n NETWORK_TYPE, --networkType=NETWORK_TYPE    (p)edestrian, (b)icycle, (c)ar, [default: pedestrian]
  -v, --verbose
  -l, --nolcc
  -c, --contract
```
#### Example
```
python run.py -f data/karlsruhe_small.osm -n p -c -v
```

## Output Format
The format looks like this
```
# Road Graph File v.0.3"
# ...
number of nodes
number of edges
id lat lon
...
s t length street_type max_speed forward backward
...
```

#### Example
```
# Road Graph File v.0.3
# number of nodes
# number of edges
# node_properties
# ...
# edge_properties
# ...
4108
4688
0 49.0163448 8.4019855
1 49.0157261 8.405539
2 49.0160334 8.4050578
...
1529 3222 102.344801043 residential 30 True False
3222 1629 7.19105938956 residential 30 True False
1629 1526 8.828179648 residential 30 True False
2306 2319 37.3600477398 track 5 True True
...
```

## Research

[Temporal Map Labeling: A New Unified Framework with Experiments](http://i11www.iti.uni-karlsruhe.de/temporallabeling/)
