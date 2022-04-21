rm *.dat
rm *.db

python3 taskC_my_parser.py ebay_data/items-*.json
sqlite3 myDatabase.db < load.txt
sqlite3 myDatabase.db < query1.sql
sqlite3 myDatabase.db < query2.sql
sqlite3 myDatabase.db < query3.sql
sqlite3 myDatabase.db < query4.sql
sqlite3 myDatabase.db < query5.sql
sqlite3 myDatabase.db < query6.sql
sqlite3 myDatabase.db < query7.sql