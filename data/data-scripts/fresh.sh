#!/bin/bash
startDate=`date`
echo "Starting at: " $startDate
find /Users/tavery/dev/doc/main/core/en/xmlsource -type f -name *.xml| tee -a rawfreshfiles.txt

input="rawfreshfiles.txt"
while IFS= read -r line
do
	echo "$line" | tee -a freshfiles.txt
	p4 fstat -Sd -T 'headModTime' $line | tee -a freshfiles.txt
done < "$input"


input="freshfiles.txt"
while IFS= read -r line
do
	sed 's/\.\.\. headModTime //;s/$/,/' | tee -a freshfiles.csv
done < "$input"

#bbedit rawfreshfiles.txt
#bbedit freshfiles.txt
bbedit freshfiles.csv

endDate=`date`
echo  "Finished at: " $endDate
#p4 fstat -Sd -T 'headAction, headType, headModTime, headTime' $line | tee -a freshfiles.txt