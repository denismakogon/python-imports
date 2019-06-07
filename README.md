# Python 3.7 imports experiment

## Purpose

As official Python 3.7 release stated that importing system implementation has changed.
Some libraries would not work out of the box (that's what happened to TensorFlow that sticks with 3.6).

The purpose of this experiment is to actually figure out if what actually changed without digging into the code
but simulating the real workload.

## Experiment details

In this experiment we're going to run two experiments:

 - [simple (raw/native or whatever) import](raw_imports.py)
 - [LRU-based (based on LRU caching) import](lru_imports.py)

Each experiment implementation you may find here:

 - [raw](test_raw.sh)
 - [lru](test_lru.sh)

I'm going to run the experiment at least 10K times (that's what might happen in production).
For this experiment we're going to use [the following system constraints](run_container.sh).

## Results

I'm going to use plot.ly and pandas to print [the results](final_results-peaks.html) of the calculations.
But here's curious observations:
```
Raw imports mean:  44487.03050305031
LRU imports mean:  39943.37513751375
Number of peaks during raw imports:  4079
Number of peaks during LRU imports:  3972
Lower mean:  39943.37513751375
Number of peaks during raw imports (higher than a lower mean):  4081
Number of peaks during LRU imports (higher than a lower mean):  3972
```

As you may see native/raw imports are slower than LRU-based imports.

At 10K - 1.1% of raw imports are slower than LRU-based imports.
At 100K - 2.3%  of raw imports are slower than LRU-based imports.


## Side note

As you may notice, I wrapped both LRU and raw import into a function that just returns an imported object.
This is necessary to measure time correctly with the same overhead.

## Disclaimer

I'm not trying to blame anyone from Python core team, but this is our reality - new imports system is slow but gets better with LRU.

Please note that this test includes only 1 import from the standard library, things might get worth with 3rd-party libraries.
The thing is that each import may act weird. But the truth is that LRU wrapper speeds up imports processing.