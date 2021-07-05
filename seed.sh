#!/bin/bash

for (( i = $2; i < $(($1 + 1)); i++ )); do
  ./db_seeder.py "$i" "$i" $((i - 1)) $((i - 1))
done
