#!/bin/bash
pwd
echo  "\n"
echo  "The list of files \n"
echo  "\n"
ls
echo  "\n"
chmod +x create_db_tables.py
echo  "\n"
python create_db_tables.py

cd hindunews/hindunews/spiders/
echo "\n"
ls

#command to run spider 
echo "\n"
echo "spider running started..................."
scrapy crawl hindunews