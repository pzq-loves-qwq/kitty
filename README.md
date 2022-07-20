# kitty
A python-lifelib based CGoL catalyst search utility. 

## Installation

`kitty` has python-lifelib as a dependency, so follow the instructions [here](https://gitlab.com/apgoucher/python-lifelib/-/blob/master/README.md) and install python-lifelib first. 

After that, just clone the repositry and you're ready. 

## Usage

`kitty` expects an input file, formatted like this: (see `example.in`):

```
active_region <pattern>
catalysts <pattern1> <pattern2> ... <patternN>
num_cats <number>
duration <number>
bounding_box <number> <number>
```

After `active_region` comes the active region you want to test. After `catalysts` comes all the catalysts you want to use.

`num_cats` refers to the number of catalysts used in the test (so it can be different from the N in `catalysts`). 

`duration` is the duration to test the catalysts. If one of the catalysts fail to recover after that many generations, the pattern is discarded. 

`bounding_box` refers to the [bounding box](https://www.conwaylife.com/wiki/Bounding_box) of the initial pattern. 

All patterns are given in headerless [RLE](https://www.conwaylife.com/wiki/RLE) format. 

After the input file is ready, run `kitty` like this:
```
$ python3 kitty.py input-file-name
```
