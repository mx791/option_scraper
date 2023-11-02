#!/usr/bin/env bash
python scraper.py >> logs/logs.txt
python send_logs.py
sudo shutdown -h now
