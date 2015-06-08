#!/bin/bash


# parse file name
filename=(`echo $1 | tr '_' ' '`)
tag=${filename[0]}

# create directory for images
mkdir $tag

# read input line-by-line
while IFS='' read -r line

do
    url=$line
    wget -P $tag $line 

done < "$1"



