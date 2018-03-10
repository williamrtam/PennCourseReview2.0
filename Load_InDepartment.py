 
# CREATE TABLE InDepartment(
# pid varchar(20),
# did varchar(20),
# PRIMARY KEY (pid, did),
# FOREIGN KEY (pid) REFERENCES Professor (pid),
# FOREIGN KEY (did) REFERENCES Department (did)
# );

import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
 
conn = db.get_connection()

query = "select pid, sid from Teaches;"
db.doQueryResults(conn,query)

cursor = conn.cursor()
cursor.execute(query)
row = cursor.fetchone()

while row is not None:
	pid = row[0]
	sid = row[1]
	dept = sid.split("-")[0]

	query_str = """insert into InDepartment (pid, did) values ('""" + pid+ """','""" + dept +"""');"""
	
	print(query_str)
	db.doQuery(conn, query_str)
	row = cursor.fetchone()

db.close(conn)
