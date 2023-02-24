#!/usr/bin/env python3

'''
# v.1
#This script creates a history of registered extensions on thirdlane. The data located in the file /var/log/impro_extension_history.log 
# git@github.com:git-improcom/thirdlane-extension-status-history.git
#
# Created on 02/22/2022
# Author: Alex Ro (alexr@improcom.com)
# Copyright (c) Improcom INC 2023
'''


import subprocess
import time
from datetime import datetime
from tabulate import tabulate

# Set file names
prev_file = "start.txt"
curr_file = "end.txt"
diff_file = "/var/log/impro_extension_history.log"

# Run extension_list_history.sh every minute
while True:
    # Get current output
    with open(curr_file, 'w') as f:
        command = "/usr/local/utils/extension_list_history/extension_list4history.sh | grep -v -e 'Improcom/2' -e 'Acrobits' -e 'Thirdlane Connect'"
        subprocess.run(command, shell=True, stdout=f) 

    with open(curr_file, 'r') as f:
        current_output = f.read().splitlines()

    # Remove unwanted lines from current output
    current_output = [line for line in current_output]

    # Compare current and previous output
    with open(prev_file, 'r') as f:
        previous_output = f.read().splitlines()
    diff_output = list(set(current_output) - set(previous_output))
    diff_output += list(set(previous_output) - set(current_output))

    # Check if there are any differences
    if diff_output:

        diff_output = [f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{'REGISTERED,' if line in current_output else 'REMOVED,'} {line}" for line in diff_output]
        data4tabulate = [line.split(',') for line in diff_output]
        diff_output_formatted = tabulate(data4tabulate)

        #print(tabulate(data4tabulate))


        # Save differences to log file
        with open(diff_file, 'a') as f:
            #f.write("\n".join(diff_output_formatted) + "\n")
            f.write(diff_output_formatted + '\n')

    # Set current output as previous output for next comparison
    subprocess.run(['cp', curr_file, prev_file])

    # Wait for 1 minute before running again
    time.sleep(60)

