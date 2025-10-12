#!/bin/sh

# Create new group using target GID
odgroup='onedrive'
groupadd "${odgroup}" -g "1000"

# Create new user using target UID
oduser='onedrive'
useradd -m "${oduser}" -u "1000" -g "1000"

RESYNC=false

echo "---------------- STARTING SYNC ---------------"
#First, we get any new data in
gosu "${oduser}" /usr/local/bin/onedrive --sync --single-directory 'exchange_folder' --confdir /onedrive/conf --syncdir /onedrive/data

echo "---------------- SYNCED, STARTING CHECK ---------------"
stat -c %y /onedrive/data/exchange_folder/last_boekhouding.gnucash
stat -c %y /onedrive/conf/last_check
#Now, we run the generate_kamp_overview if the edit date of the last boekhouding file is newer than the last_check file
#[ /onedrive/data/exchange_folder/last_boekhouding.gnucash -nt /onedrive/conf/last_check ] || python3 /scratch/generate_kamp_overview.py
if [ /onedrive/data/exchange_folder/last_boekhouding.gnucash -nt /onedrive/conf/last_check ]; then
    python3 /scratch/generate_kamp_overview.py
    RESYNC=true
fi

if [ /onedrive/data/exchange_folder/declaraties -nt /onedrive/conf/last_check_declaraties ]; then
    python3 /scratch/build_declaration.py
    RESYNC=true
fi



if $RESYNC; then
  echo "---------------- RE-SYNCING ---------------"
  gosu "${oduser}" /usr/local/bin/onedrive --sync --single-directory 'exchange_folder' --confdir /onedrive/conf --syncdir /onedrive/data
fi


#Finally, we update the last_check file to reflect the current time we checked if it was older than the boekhouding file
echo "---------------- UPDATING CHECK FILES ---------------"
touch /onedrive/conf/last_check
touch /onedrive/conf/last_check_declaraties