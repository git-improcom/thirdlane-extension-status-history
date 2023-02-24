# thirdlane-extension-status-history
Utility to collect the status of registered extensions each minute. Created for multitenant thirdlane and gets the data from Kamailio

## Description
Consist of next files:  
* extension_history.py - script that supposed to run as a service
* extension_list4history.sh - get information about registered extensions from the database. DB credentials are extracted from /etc/odbc.ini
* etc/systemd/system/impro-extension-history.service - service file
Note, that the path where the script is supposed to run is hardcoded: /usr/local/utils/
If you do not like it you need to update it in all files.
The script is supposed to be run on CentOS with systemd. Also, you can run the script manually and keep it in terminal.

## Requirements
bash, awk  
python3 with 
```
import subprocess
import time
from datetime import datetime
from tabulate import tabulate
```


## INSTALL
```
mkdir /usr/local/utils/
cp -prf extension_list_history /usr/local/utils/
cp etc/logrotate.d/impro-extension-history /etc/logrotate.d/impro-extension-history
cp etc/systemd/system/impro-extension-history.service /etc/systemd/system/impro-extension-history.service
systemctl enable impro-extension-history
systemctl start impro-extension-history
```

## USAGE
The logfile is located here: /var/log/impro_extension_history.log  
The statistic is collected every minute
