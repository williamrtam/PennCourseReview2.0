 
# CREATE TABLE Offered(
# code varchar(20),
# did varchar(20),
# sid varchar(20),
# semid varchar(20),
# PRIMARY KEY(sid),
# FOREIGN KEY(sid) REFERENCES Section (sid),
# FOREIGN KEY(semid) REFERENCES Semester (semid),
# FOREIGN KEY(did) REFERENCES Department (did) ON DELETE CASCADE,
# FOREIGN KEY(code) REFERENCES Course (code) ON DELETE CASCADE
# );

import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr


conn = db.get_connection()

section_query = "select sid from Section;"
db.doQueryResults(conn,section_query)

cursor = conn.cursor()
cursor.execute(section_query)
row = cursor.fetchone()

while row is not None: 
	info = row[0].split("-")
	code = info[0] + "-" + info[1]
	dept = info[0]
	sem = info[-1] #last thing 
	sid = row[0]

	query_str = """insert into Offered(code, did, sid, semid) values ('""" + code + """','""" + dept + """','"""+ sid + """','""" + sem + """');"""
	print(query_str)
	db.doQuery(conn, query_str)
	row = cursor.fetchone()

db.close(conn)