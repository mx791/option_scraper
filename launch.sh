#!/usr/bin/env bash
python /home/ec2-user/option_scraper/scraper.py >> /home/ec2-user/option_scraper/logs.txt
python /home/ec2-user/option_scraper/send_logs.py
sudo shutdown -h now
