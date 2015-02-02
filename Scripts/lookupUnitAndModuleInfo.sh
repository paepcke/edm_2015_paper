#!/bin/bash

# Input file:
#     video_id, video_code, resource_display_name,page 
# Page entries:
#     https://class.stanford.edu/.../coursware/495757ee7b25401599b1ef0495b068e4/4fe1ef4953674903b88a0c9bf344
# Get 4957... into $unitId, and 4fe1... into $moduleId

USAGE='`basename $0` [-u localMySQLUser][-p][-pLocalMySQLPwd] <fileWithVideoPageLogEntries>' 
# If option -p is provided, script will request password for
# local MySQL db. If pwd is omitted, script checks in ~/.ssh/mysql
# for pwd.


if [[ "$#" < 1 ]]
then
    echo $USAGE
    exit
fi

pageURLFile=$1
#lookupScript=/home/dataman/Code/json_to_relation/Scripts/lookupOpenEdxHash.py
lookupScript=/home/paepcke/EclipseWorkspaces/json_to_relation/scripts/lookupOpenEdxHash.py

#lookupScript=/home/dataman/Code/json_to_relation/Scripts/lookupTest.csv
lookupTestFile=/home/paepcke/EclipseWorkspaces/json_to_relation/scripts/lookupTest.csv

# --------------------------- Actual Processing ---------

echo "video_id,unitLabel,moduleLabel"

# Read one page ID at a time, and
# extract the second-to-last, and last
# element of the url:
while read oneVideoInfoLine
do
  # Read one line into a bash array.
  # Only first element will be filled:
  
  IFS=$'\n' lineArr=($(cat ${pageURLFile}))
  # Fill each line into a slot in $lineArr:
  for i in $(seq ${#lineArr[*]}); do
      [[ ${lineArr[$i-1]} = $name ]] && echo "${lineArr[$i]}"
  done

  # Get each column of the first (and only) line
  # into an array:
  IFS=$',' colArr=(${lineArr[0]})

  # The video_id:
  videoId=${colArr[0]}

  # Number of columns, and position of the page URL:
  colArrLen=${#colArr[@]}
  pagePos=$((length - 1))

  # Get the page column:
  pageUrl=${colArr[$pagePos]}

  # Remove slashes, replacing them by spaces:
  #IFS=$'/' 
  pageUrl="${pageUrl//\// }"

  # Turn the elements of the page URL into an array:
  IFS=' ' read -a pageUrlArr <<<${pageUrl}

  pageUrlArrLen=${#pageUrlArr[@]}

  # Positions of Unit and Module identifiers
  # in the array-ified page URL:
  unitPos=$((pageUrlArrLen - 2))
  modulePos=$((pageUrlArrLen - 1))

  unitId=${pageUrlArr[${unitPos}]}
  moduleId=${pageUrlArr[${modulePos}]}

  #$lookupScript ${unitId} ${moduleId}
  unitLabel=$(${lookupScript} ${unitId})
  moduleLabel=$(${lookupScript} ${moduleId})

  echo $videoId,\"$unitLabel\",\"$moduleLabel\"

done <$pageURLFile
