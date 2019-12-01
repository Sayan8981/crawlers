 
#!/bin/bash
pwd
echo  "\n"
echo  "The list of files \n"
echo  "\n"
ls
echo  "\n"
chmod +x create_db_tables_ceva_shipment.py
echo  "\n"

echo "Please enter your database_username"
read username
echo  "\n"
echo "Please enter your database_password"
read password

python create_db_tables_ceva_shipment.py "$username" "$password"

cd CEVA_shipment_track/CEVA_shipment_track/spiders/
pwd
echo "\n"
ls

#command to run spider 
echo "\n"
echo "spider running started..................."
scrapy crawl ceva_shipment