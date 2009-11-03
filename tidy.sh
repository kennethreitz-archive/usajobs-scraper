#!/bin/bash
FILES="./pages/*"
for f in "$FILES"
do
  echo "Processing $f file..."
  tidy $f > output
done