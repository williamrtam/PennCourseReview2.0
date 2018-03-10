import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
conn = db.get_connection()

f = open('registrar_data.csv', 'r')

for line in f:
    vals = line.split(",")
    sec_code = vals[0]
    term = vals[1]
    start_time = vals[2]
    end_time = vals[3]
    meeting_days = vals[4]

    query_str = "insert into CourseListing(secid,semid,start_time,end_time,days) values('{0}','{1}',{2},{3},'{4}');".format(sec_code,term,start_time,end_time,meeting_days)
    print query_str
    db.doQuery(conn,query_str)

db.close(conn)
