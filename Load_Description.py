import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
import DynamoDB_calls as db

table = db.getTable()

conn = db.get_connection()
query_str = """select code, semid from Offered;"""
res = db.doQueryResults(conn,query_str)
for tup in res:
	code = tup[0]
	semid = tup[1]
	# check if course has already been collected for
	res = getItem(table, code)
	if res is None:
		# there is no entry for this course yet
		str = "/courses/{0}-{1}".format(semid, code)
		http_str = set_http_pcr(str) 
		json_obj = get_request_pcr(http_str)
		pcr_res = json_obj["result"]
		if json_obj["valid"]:
			desc = pcr_res["description"]
			db.insertItem(table, code, desc)
		else: 
			print pcr_res["error"]
db.close(conn)

