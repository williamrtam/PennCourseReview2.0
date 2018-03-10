import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr


conn = db.get_connection()

http_str = set_http_pcr("depts")
json_obj = get_request_pcr(http_str)
dept_list = json_obj["result"]["values"]
for dept in dept_list:
	# leave school as null because we dont know if we can get that
	http_str = set_http_pcr(dept["path"])
	json_obj = get_request_pcr(http_str)
	course_list = json_obj["result"]["coursehistories"]
	for course in course_list:
		alias_list = course["aliases"]
		#print course
		code = alias_list[0]
		split = code.split("-")
		did = split[0]
		name = course["name"]
		query_str = "Select * from Course where code='{0}';".format(code)
		res = db.doQueryResults(conn,query_str)
		if res is None:
			query_str = """Insert into Course (code,name,quality,difficulty,did) values ("{0}","{1}",-1,-1,"{2}");""".format(code,name,did)
                	db.doQuery(conn,query_str)
			print "Added course: " + code
		else:
			print "Course exists:" + code 

		for alias in alias_list:
			#print alias
			query_str = "Select alias from Alias where code='{0}';".format(alias)
                	res = db.doQueryResults(conn,query_str)
			if res is None:
				# add to alias table with this code as the primary alias
				query_str = "Insert into Alias (alias,code) values ('{0}','{1}');".format(alias,code)
				db.doQuery(conn,query_str)
				print "Added: " + alias + " with alias: " + alias_list[0]
				#print "Error: Could not find alias in Alias table..",alias_list[0]
			else:
				print "already have an alias for " + alias


db.close(conn)
