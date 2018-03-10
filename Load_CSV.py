import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
conn = db.get_connection()
from penn import Registrar

#Jack Token - locked for now
REG_USERNAME = 'UPENN_OD_enka_1003904'
REG_PASSWORD = '8enqh1mlsj4ed7oj3nvk44c84s'

#Siyin Tokem - take 2
# REG_USERNAME = 'UPENN_OD_enlM_1004004'
# REG_PASSWORD = 'vniqedjjt2i8gcescopkcjrjrq'
with open("registrar_data.csv", "w") as csv_file:
    r = Registrar(REG_USERNAME, REG_PASSWORD)
    query_str = 'Select code from Course;'
    courses = db.doQueryResults(conn,query_str)
    for course in courses:
        done = False
        split = course[0].split("-")
        dept = split[0]
        c_num = split[1]
        #s_num = '001'
        query_str = "select sid from Section where sid like '{0}%';".format(course[0]);
        sections =db.doQueryResults(conn,query_str)
        if sections is None:
            continue
        for section in sections:
            split = section[0].split("-")
            s_num = split[2]
            sec_code = split[0]+"-"+split[1]+"-"+split[2]
            try:
                print sec_code
                listing = r.section(dept, c_num, s_num)
                if listing is None:
                    continue;
                else:
                    for meeting in listing["meetings"]:
                        start_time = meeting["start_time_24"]
                        end_time = meeting["end_time_24"]
                        meeting_days = meeting["meeting_days"]
                        term = meeting["term"]
                        line = '' + str(sec_code) + ',' + str(term) + ',' + str(start_time) + ',' + str(end_time) + ',' + meeting_days + '\n'
                        print ('putting ' + line)
                        csv_file.write(line)
            except ValueError:
                print "Course section not found: %s-%s-%s" % (dept, c_num, s_num)
db.close(conn)
