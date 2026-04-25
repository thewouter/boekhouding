#!/bin/sh


RESYNC=false

# Desired IDs
TARGET_UID=1000
TARGET_GID=1000



# Check if a group with GID=1000 already exists
existing_group=$(getent group "$TARGET_GID" | cut -d: -f1)
if [ -n "$existing_group" ]; then
    odgroup="$existing_group"
    echo "Using existing group '$odgroup' (GID=$TARGET_GID)"
else
    odgroup='onedrive'
    echo "Creating new group '$odgroup' (GID=$TARGET_GID)"
    groupadd -g "$TARGET_GID" "$odgroup"
fi

# Check if a user with UID=1000 already exists
existing_user=$(getent passwd "$TARGET_UID" | cut -d: -f1)
if [ -n "$existing_user" ]; then
    oduser="$existing_user"
    echo "Using existing user '$oduser' (UID=$TARGET_UID)"
else
    oduser='onedrive'
    echo "Creating new user '$oduser' (UID=$TARGET_UID, GID=$TARGET_GID)"
    useradd -m -u "$TARGET_UID" -g "$TARGET_GID" "$oduser"
fi

echo "---------------- STARTING SYNC ---------------"
#First, we get any new data in
/usr/sbin/gosu "${oduser}" /usr/local/bin/onedrive --sync --verbose --single-directory 'exchange_folder' --confdir /onedrive/conf --syncdir /onedrive/data

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

if [ /onedrive/data/exchange_folder/inschrijvingen -nt /onedrive/conf/last_check_inschrijvingen ]; then
    python3 /scratch/generate_enroll_forms.py
    RESYNC=true
fi



if $RESYNC; then
  echo "---------------- RE-SYNCING ---------------"
  /usr/sbin/gosu "${oduser}" /usr/local/bin/onedrive --sync --single-directory 'exchange_folder' --confdir /onedrive/conf --syncdir /onedrive/data
fi


#Finally, we update the last_check file to reflect the current time we checked if it was older than the boekhouding file
echo "---------------- UPDATING CHECK FILES ---------------"
touch /onedrive/conf/last_check
touch /onedrive/conf/last_check_declaraties
