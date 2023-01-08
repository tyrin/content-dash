#!/bin/bash

if [ ! -f 'rawfreshfiles.txt' ]
then
  echo "rawfreshfiles.txt does not exist. Skipping..."
else
  rm 'rawfreshfiles.txt'
fi

if [ ! -f 'freshfiles.txt' ]
then
  echo "freshfiles.txt does not exist. Skipping..."
else
  rm 'freshfiles.txt'
fi

if [ ! -f 'freshfiles.csv' ]
then
  echo "freshfiles.csv does not exist. Skipping..."
else
  rm 'freshfiles.csv'
fi