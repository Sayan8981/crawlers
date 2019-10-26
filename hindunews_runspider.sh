#!/bin/bash
pwd
echo  "\n"
echo  "The list of files \n"
echo  "\n"
ls
echo  "\n"
chmod +x create_db_tables.py
echo  "\n"

echo "Please enter your database_username"
read username
echo  "\n"
echo "Please enter your database_password"
read password

python create_db_tables.py "$username" "$password"

cd hindunews/hindunews/spiders/
echo "\n"
ls

#command to run spider 
echo "\n"
echo "spider running started..................."
scrapy runspider hindunews_browse.py