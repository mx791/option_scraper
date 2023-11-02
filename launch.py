#!/usr/bin/env bash
cd /home/ec2-user/option_scraper
git pull --force >> logs.txt
pip install -r requirements.txt
python scraper.py >> logs.txt
python send_logs.py
