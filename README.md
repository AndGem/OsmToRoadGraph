# OsmToRoadGraph v.0.3

[![Build Status](https://travis-ci.org/AndGem/OsmToRoadGraph.svg?branch=master)](https://travis-ci.org/AndGem/OsmToRoadGraph)
[![codecov](https://codecov.io/gh/AndGem/OsmToRoadGraph/branch/master/graph/badge.svg)](https://codecov.io/gh/AndGem/OsmToRoadGraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- TOC -->

- [OsmToRoadGraph v.0.3](#osmtoroadgraph-v03)
- [Introduction](#introduction)
    - [Motivation](#motivation)
    - [Description](#description)
    - [Requirements](#requirements)
    - [Usage](#usage)
        - [Usage - Explanation](#usage---explanation)
        - [Example](#example)
        - [Output](#output)
            - [Output Format](#output-format)
                - [Example Road Network (*.pycgr)](#example-road-network-pycgr)
                - [Example Street Names (*.pycgr_names)](#example-street-names-pycgr_names)
    - [Research](#research)

<!-- /TOC -->

# Introduction
OSMtoRoadGraph aims to provide a simple tool to allow extraction of the road network of [OpenStreetMap](http://www.openstreetmap.org) files. It differentiates between three transportation networks: car, bicycle, and walking. The output data depends on the chosen parameters (which street highway types to consider, speed, ...).

## Motivation
OpenStreetMap provides free cartographic data to anyone. Data can be added and edited by anyone. However, using the road network contained in the OSM files is not straightforward. This tool aims to reduce the overhead of writing a parser for OSM files.

## Description
With this tool the data is being converted into easily parsable plaintext files that can be used by any application for further processing. For each transportation network type two output files are generated. One file contains the nodes (with coordinates), and the network edges, with length, direction and maximum speed (according to chosen network type). The second file contains street names that could be extracted for all edges contained in the first file.

## Requirements
* Python 2.7+/Python 3.6+/PyPy
* [future package](https://pypi.python.org/pypi/future) 
    * to install run `pip install -r requirements.txt`
* An OSM XML file

## Usage
```
Usage: run.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
  -n NETWORK_TYPE, --networkType=NETWORK_TYPE    (p)edestrian, (b)icycle, (c)ar, [default: pedestrian]
  -l, --nolcc
  -c, --contract
```
### Usage - Explanation

`-f` points to the input filename; the output files will be created in the same folder and using the name of the input file as prefix and adding information as suffix.

`-n` sets the network type. This influences the maximum speed saved for the edges. If you care only about connectivity set it to pedestrian.

`-l` if you set this option the graph will be output as a whole but _may_ contain unconnected compoonents. By default the largest connected component is determined and the rest is dropped.

`-c` if you specify this option additional to the original graph, a second pair of filenames will be created containing the result of contracting all degree 2 nodes.

### Example
```
python run.py -f data/karlsruhe_small.osm -n p -v
```

### Output

The output will consist of two plaintext files. One file ending in `.pypgr`, `pybgr`, or `pycgr` depending on the network type selected; the other file will have the same ending with a `_names` as additional suffix. The first file contains the graph structure as well as additional information about the edge (length, max speed according to highway type, if it is a one-way street or not). The file ending with `_names` includes the street names for the edges. 


#### Output Format
The structure of the road network output file is the following:
```
<HEADER LINES STARTING WITH A DASH(#) CHARACTER>
<number of nodes>
<number of edges>
<id> <lat> <lon>
...
<s> <t> <length> <street_type> <max_speed> <forward> <backward>
...
```

##### Example Road Network (*.pycgr)
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

##### Example Street Names (*.pycgr_names)
```
Hölderlinstraße
Hölderlinstraße
Hölderlinstraße

Kronenstraße
Kronenstraße
Kronenstraße

Zähringerstraße
Zähringerstraße
```
Each line consists of a street name. The number in which a line is corresponds to the edges index. In this example this means, that Hölderlinstraße is the street name of edges 0, 1, 2. The absence of a name in line 4 indicates that edge 3 has no street name. Edges 4, 5, 6 have street name Kronenstraße, and so on...

## Research

[Temporal Map Labeling: A New Unified Framework with Experiments](http://i11www.iti.uni-karlsruhe.de/temporallabeling/)
