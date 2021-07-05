#!/bin/bash

while true; do
  python vrp_test.py
  if [ $? -ne 0 ]; then
    exit $?
  fi
done
