Note: this process is designed to run on Mac OS in the terminal. It can be adapted for Windows, but not with the current files.
To generate freshness data:
1) Copy the fresh.sh and freshdate.sh scripts into the top-level folder that you want to generate data for.
	If you want to generate the standard file, this is the /Users/(your_machine)/dev/doc/main/core/en/xmlsource directory
3) Call fresh.sh This generates two files
	The script gets a list of all the files in every subdirectory of the current directory
	specified in the first line of the script. This takes 60 secs to run and
	produces "rawfreshfiles.txt" as output. The headModTime is a number in seconds.

	The script runs the p4 fstat command to get the headModTime for each file in the rawfreshfiles.txt
	The headModTime is the last time the file was modified on the client, before it was submitted
	to the depot, so avoids branching or integration date updates. If you do the full file set, this script takes hours (approx 14) to run and
	produces "freshfiles.txt" as output. I highly recommend that you run it overnight.

	The script uses freshfiles.txt as input and fixes the formatting to produce freshfiles.csv
	freshfiles.csv
	The script will open the outputfiles in bbedit automatically.
	**Note**: If you need to call the scripts more than once, use cleanfresh.sh to remove the previous file artefacts.
	If you don't remove them, then the text is added to the end of the file, rather than replacing it.
	(i.e. you won't get the results you want)
4) Examine freshfiles.csv, add column headings, remove machine specific parts of the path, etc.
5) Generate a date:
	Copy the values from the headModTime in the csv file into a new file called freshsecs.txt.
	Save the file in the same directory as the freshdate.sh script.
6) Run freshdate.sh and copy the values from the freshdates.txt output file into the freshfiles.csv.
7) Add an excel formula to the csv to generate a group name

Note: regex to extract the group is:
^([^:]*:){1}([^:]*)
And extract \2 for the second capture group
This approach avoids issues where there's only a portal and not a group
But you'll have an issue in that some lines won't have anything but a portal
