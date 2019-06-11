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

```bash
6514 LRU imports were faster than raw imports
3485 raw imports were slower than LRU imports

Range: [0:20000]
Number of raw imports in range: 5853
Number of LRU imports in range: 6003
Raw imports mean: 9981.924483171024
LRU imports mean: 7118.146926536731
Practical percentage of slow imports in range [0: 20000]: 40.2320658197995


Range: [20000:40000]
Number of raw imports in range: 65
Number of LRU imports in range: 24
Raw imports mean: 24157.169230769232
LRU imports mean: 26521.791666666668
Practical percentage of slow imports in range [20000: 40000]: -8.915771851376697


Range: [40000:60000]
Number of raw imports in range: 18
Number of LRU imports in range: 25
Raw imports mean: 53170.666666666664
LRU imports mean: 51157.84
Practical percentage of slow imports in range [40000: 60000]: 3.9345419327060593


Range: [60000:80000]
Number of raw imports in range: 91
Number of LRU imports in range: 253
Raw imports mean: 74713.51648351649
LRU imports mean: 75567.77075098814
Practical percentage of slow imports in range [60000: 80000]: -1.1304478866878354


Range: [80000:618199]
Number of raw imports in range: 3972
Number of LRU imports in range: 3694
Raw imports mean: 94933.38267875125
LRU imports mean: 90858.0013535463
Practical percentage of slow imports in range [80000: 618199]: 4.485440208338787


Range: [0:60000]
Number of raw imports in range: 5936
Number of LRU imports in range: 6052
Raw imports mean: 10268.108490566037
LRU imports mean: 7377.016688697951
Practical percentage of slow imports in range [0: 60000]: 39.190528148017044

```

As you may see, at most of the times, native/raw imports theoretically are slower than LRU-based imports.
In particular, 6514 times raw/native import is slower than LRU-based import.

The time difference could be up to 39% in the most effective range from zero up to 20K, 
this range contains at least like a half of all imports.

Each range visualization you may find in the following folders:

 - [1st run](visual/1st_run) is where you'd find 20K-step imports time analytics
 - [2nd run](visual/2nd_run) is where you'd find 0-60K, 60K and beyond ranges visualized

## Side note

As you may notice, I wrapped both LRU and raw import into a function that just returns an imported object.
This is necessary to measure time correctly with the same overhead.

## Disclaimer

I'm not trying to blame anyone from Python core team, but this is our reality - new imports system is slow but gets better with LRU.

Please note that this test includes only 1 import from the standard library, things might get worth with 3rd-party libraries.
The thing is that each import may act weird. But the truth is that LRU wrapper speeds up imports processing.

## Downsides

Okay, my approach has couple disadvantages:

    - ugly hack
    - for monolith applications may not be necessary
    - breaks native development/debugging flow
    - if nobody taking all of that seriously then why should I care?


## Advantages

It works better than ordinary imports.
The best area to apply the following knowledge - serverless (due to the "cold start issue").
