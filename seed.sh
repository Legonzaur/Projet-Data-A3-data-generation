#!/bin/bash

for (( i = 10; i < $1; i++ )); do
  ./db_seeder.py "$i" "$i" $((i - 1)) $((i - 1))
done