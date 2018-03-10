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

query = "select code, AVG(num_reviews) from (select * from Section  S) as s inner join Offered o on o.sid = s.sid group by code; "
db.doQueryResults(conn,query)

cursor = conn.cursor()
cursor.execute(query)
row = cursor.fetchone()

while row is not None:
	code = row[0]
	avg_num_reviews = row[1]

	query_str = """update Course set avg_num_reviews = '""" + str(avg_num_reviews)+ """' where Course.code = '""" + code+ """' ;"""
	
	print(query_str)
	db.doQuery(conn, query_str)
	row = cursor.fetchone()

db.close(conn)