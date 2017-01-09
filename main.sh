#!/bin/bash

echo -n "Enter subject ID: "
read subject_ID
echo -n "Choose condition: diffuse (d), clustered (c), or random (r): "
read condition
echo -n "Debug (f = false, t = true): "
read debug

./scrabble_practice.py 
./scrabble_pretest.py $subject_ID $condition $debug

./visual_foraging_practice.py $condition $debug
./intro_foraging.py
./visual_foraging.py $subject_ID $condition $debug

./intro_scrabble_posttest.py
./scrabble_posttest.py $subject_ID $condition $debug

