#!/usr/bin/bash

# Input file:
#     video_id, video_code, resource_display_name,page 
# Page entries:
#     https://class.stanford.edu/.../coursware/495757ee7b25401599b1ef0495b068e4/4fe1ef4953674903b88a0c9bf344


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
lookupScript=/home/dataman/Code/json_to_relation/Scripts/lookupOpenEdxHash.py

# --------------------------- Actual Processing ---------

# Read one page ID at a time, and
# extract the second-to-last, and last
# element of the url:
while read oneVideoInfoLine
do
  # Read the URL into a Bash array:
  IFS='/' read -a urlArr <<< "onePageURL"
  unitId=${urlArr[-2]}
  moduleId=${urlArr[-1]}
  echo $lookupScript ${unitId},${moduleId}
done <$pageURLFile
