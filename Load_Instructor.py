import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr


conn = db.get_connection()
print("Currently in db:")
db.doQuery(conn, "select count(*) from Professor;")
http_str = set_http_pcr("instructors")
json_obj = get_request_pcr(http_str)
instr_list = json_obj["result"]["values"]
for item in instr_list:
        # need to use tripple quotes because some names have ' in them
        # instructors have -1 as default avg rating
    pid = "{0}".format(item["id"])
    just_the_num = pid.split("-")[0]
    query_str = """insert into Professor (pid,name,avg_rating) VALUES("{0}","{1}",-1);""".format(just_the_num,item["name"])
    db.doQuery(conn,query_str)
db.close(conn)

