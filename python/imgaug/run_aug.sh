#!/bin/bash

for ((i=0; i<$1; i=i+1));
do
    {
    echo $i
    python vt_aug.py -c $2 -i $i -s $1
}&
done
wait
echo $2
python combine_img.py -c $2 -s $1