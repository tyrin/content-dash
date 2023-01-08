#!/bin/bash

#date -r 1316150979

input="freshsecs.txt"
while IFS= read -r line
do
	echo "$line"
	date -r $line | tee -a freshdates.txt
done < "$input"

bbedit freshdates.txt