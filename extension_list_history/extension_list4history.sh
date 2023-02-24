#!/bin/bash

# v.1 
#This script gets list of registered extensions on thirdlane. Note that it has a delay about 30 seconds since the actual registration time.
# git@github.com:git-improcom/thirdlane-extension-status-history.git
#
# Created on 02/22/2022
# Author: Alex Ro (alexr@improcom.com)
# Copyright (c) Improcom INC 2023

# Path to the configuration file
CONFIG_FILE="/etc/odbc.ini"

# Extract User, Password, and Database from the section

# /\[pbxconf\]/ ...if line == [pbxconf] then we set flag=1 and move to next line. All lines with f==1 will be withing our section...
# Second pattern check...  if /^\[/ (line starts from "[" then we set flag=0. It means that the next section started. 
# if (flag==1 ...it means that we are within our section... && $1 ~ "Password" ...first argument matched variable we are looking for...  then {gsub(/ /,"") ...remove extra spaces... print $2; exit ...stop execution - we found our var...}

USER=$(awk -F "=" '/\[pbxconf\]/{ flag=1; next } /^\[/{flag=0; next} (flag==1 && $1 ~ "User") {gsub(/ /,""); print $2; exit}' "$CONFIG_FILE")
PASSWORD=$(awk -F "=" '/\[pbxconf\]/{ flag=1; next } /^\[/{flag=0; next} (flag==1 && $1 ~ "Password") {gsub(/ /,""); print $2; exit}' "$CONFIG_FILE")
DATABASE=$(awk -F "=" '/\[pbxconf\]/{ flag=1; next } /^\[/{flag=0; next} (flag==1 && $1 ~ "Database") {gsub(/ /,""); print $2; exit}' "$CONFIG_FILE")

echo "select CONCAT_WS(',',username,contact,received,user_agent) from location order by substring_index(username,'-',-1), username;" | mysql -h 127.0.0.1 -s -u ${USER} -p${PASSWORD} ${DATABASE}
