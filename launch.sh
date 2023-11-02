#!/usr/bin/env bash
cd /home/ec2-user/option_scraper
git reset --hard HEAD
git pull --force > logs.txt
sudo chmod 777 launch.sh
# pip install -r requirements.txt
python scraper.py >> logs.txt
python send_logs.py
