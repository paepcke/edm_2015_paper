#!/bin/bash

# Assume we are in directory with all the heatmap files.
# File names are of form:
#   heatVals_i4x-Medicine-MedStats-video-9fdc173ccb8a48dc8777f5ccf1d48e50_SpclLrnrsTop20.csv
# Takes an output file (which can be /dev/stdout). Fills
# that file with a tab-separated table of all heatmap derivatives in
# the directory. All .csv files in the current directory
# are assumed to be heatfiles: two columns: second,numViews
# without column header.
#
# The result will have a header line: second\t<vid_code1>\t<vid_code2>\t...

USAGE="Usage: createNumviewDerivative.sh <outFile>"

if [[ "$#" < 1 ]]
then
    echo $USAGE
    exit
fi

outFile=$1
derivationScript=/home/dataman/Code/discrete_differentiator/src/discrete_differentiator/discrete_differentiator.py

# -------------- Support Functions -----------------

ensureNoDuplicates () {
  # Go through colHeaders array and exit script if
  # there is a duplicate
  local el
  local foundOne
  local candidate
  for el in "${colHeaders[@]}"
  do
      foundOne=0
      for candidate in "${colHeaders[@]}"
      do
          if [[ $candidate == $el ]]
	  then
	      if [[ $foundOne > 0 ]]
	      then
		  echo "Found duplicate: $el"
		  exit -1
              else
		  foundOne=1
	      fi
          fi
      done
  done
}

# -------------- Prep  -----------------

# Grab file names into an array:
currDir=`pwd`
fileNameArr=(`find $currDir -name "*.csv"`)

# Make a parallel array with column names derived from the file names;
# we make the names by taking the last 4 hex digits from the interior
# of the file name:
numDigitsNeeded=4

declare -a colHeaders
for fileName in "${fileNameArr[@]}"
do
    # Get the hex code part of the file name (see ex. at top of this file):
    hexPart=`echo $fileName | sed -n 's/.*video-\([^_]*\).*/\1/p'`
    lastNDigits=${hexPart:${#hexPart} - $numDigitsNeeded}
    colHeaders+=('der_vid_'$lastNDigits)
done
# If 4 digits weren't enough for uniqueness,
# the following will bomb out of this script:
ensureNoDuplicates
# If we get here: no dups.


# -------------- Fold Derivatives of View Counts Into the Outfile as Columns  -----------------

tmpFile=`mktemp -t derivativeTmp_XXXXXXXXXXXXX.tab`
tmpFile1=`mktemp -t derivativeTmp_XXXXXXXXXXXXX.tab`

# Create 0th column: rising number of ints: the seconds:
for second in `seq 0 2500`
do
    echo $second >> $tmpFile
done

for fileName in "${fileNameArr[@]}"
do
    # With one heatfile after the other:
    # grab the second col (the numViews),
    # and append its derivative as a 
    # column to the existing
    # columns in tmpFile. The dash says to 
    # add at end of existing columns. The
    # -i tells derivation script that the 
    # sequence to take the derivative of in
    # this file is the second col (zero-based):

    # Make the derivative
    $derivationScript -i 1 $fileName | paste $tmpFile - > $tmpFile1

    # Make the new file the old one for 
    # the next column appending:
    mv $tmpFile1 $tmpFile
done

# Add the CSV header:

# Col0 is the seconds:
printf 'second\t' > $outFile
# Need the sed expression to remove the trailing tab:
printf '%s\t' "${colHeaders[@]}" | sed -n 's/\(.*\)\t$/\1\n/p' >> $outFile

cat $tmpFile >> $outFile
rm $tmpFile


