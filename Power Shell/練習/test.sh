#!/bin/bash
for i in 1 2 3 4 5
do
    echo $((RANDOM % 10 + 1))
done