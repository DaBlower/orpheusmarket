#!/bin/bash
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
logfile="/home/olive/backup-bm-api/logs/$timestamp.log"
/home/olive/backup-bm-api/venv/bin/python /home/olive/backup-bm-api/main.py >> "$logfile" 2>&1
