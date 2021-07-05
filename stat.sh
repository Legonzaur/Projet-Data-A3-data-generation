#!/bin/bash

default_iterations=1000
default_init_pop=8
default_graph_size=10

iterations=$1
init_pop=$2
graph_size=$3

# iterations
for (( i = default_iterations; i < iterations; i++ )); do
    ./vrp_test_complete.py "$i" $default_init_pop $default_graph_size >> stats_iterations.txt
done

# initial population
for (( i = default_init_pop; i < init_pop; i++ )); do
    ./vrp_test_complete.py $default_iterations "$i" $default_graph_size >> stats_population.txt
done

# graph size
for (( i = default_graph_size; i < graph_size; i++ )); do
    ./vrp_test_complete.py $default_iterations $default_init_pop "$i" >> stats_graph_size.txt
done