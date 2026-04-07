#!/bin/bash

echo "Start test"

# test whether wc -l counts \n as a valid line & adds to its total count
var=$'test\ntest\ntest\ntest\n' # returns 5, each \n is an extra line
n_lines=$(echo "$var" | wc -l)
echo $n_lines

echo "End test"