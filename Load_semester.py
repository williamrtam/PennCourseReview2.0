import requests 
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr 
 

conn = db.get_connection()
print("Currently in db:")
db.doQuery(conn, "select * from Semester;")

http_str = set_http_pcr("semesters")
json_obj = get_request_pcr(http_str)
sem_list = json_obj["result"]["values"]
for item in sem_list:
	# need to use tripple quotes because some names have ' in them
	# leave school as null because we dont know if we can get that
	query_str = """INSERT INTO Semester (semid,name) VALUES ("{0}","{1}");""".format(item["id"],item["name"])
	print(query_str)
	db.doQuery(conn,query_str)
db.close(conn)

