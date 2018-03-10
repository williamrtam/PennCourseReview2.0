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

query = "select pid, AVG(InstructorQuality) from (select * from Teaches t where t.InstructorQuality > -1) as filtered group by pid;"
db.doQueryResults(conn,query)

cursor = conn.cursor()
cursor.execute(query)
row = cursor.fetchone()

while row is not None:
	pid = row[0]
	avg_rating = row[1]

	query_str = """update Professor set avg_rating = '""" + str(avg_rating)+ """' where Professor.pid = '""" + pid+ """' ;"""
	
	print(query_str)
	db.doQuery(conn, query_str)
	row = cursor.fetchone()

db.close(conn)
