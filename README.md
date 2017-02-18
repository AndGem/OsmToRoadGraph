# OsmToRoadGraph v.0.1

[![Build Status](https://travis-ci.org/AndGem/OsmToRoadGraph.svg?branch=master)](https://travis-ci.org/AndGem/OsmToRoadGraph)
[![codecov](https://codecov.io/gh/AndGem/OsmToRoadGraph/branch/master/graph/badge.svg)](https://codecov.io/gh/AndGem/OsmToRoadGraph)

<!-- TOC -->

- [OsmToRoadGraph v.0.1](#osmtoroadgraph-v01)
- [Introduction](#introduction)
    - [Requirements](#requirements)
    - [Usage](#usage)
            - [Example](#example)
    - [Output Format](#output-format)
            - [Example](#example-1)

<!-- /TOC -->

# Introduction

Converting [OpenStreetMap's](http://www.openstreetmap.org) OSM XML files to a simple graph format for further processing.

## Requirements
* Python 2.7+/Python 3.6
* `future` package
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
node_properties
...
edge_properties
...
```

#### Example
```
# Road Graph File v.0.3
# number of nodes
# number of edges
# node_id node_properties
# ...
# s_id t_id edge_properties
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
```