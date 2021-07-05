#!/bin/bash

for (( i = 10; i < $1; i++ )); do
    ./vrp_test_complete.py "$i" >> speed.txt
done