#!/usr/bin/env bash


for i in {1..10000};
 do python /code/raw_imports.py 2>&1 |  grep "| collections" | awk '{print $5}';
done
