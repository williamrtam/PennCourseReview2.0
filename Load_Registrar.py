import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
conn = db.get_connection()
from penn import Registrar

#Jack Token
# REG_USERNAME = 'UPENN_OD_enka_1003904'
# REG_PASSWORD = '8enqh1mlsj4ed7oj3nvk44c84s'

#Siyin Token
REG_USERNAME = 'UPENN_OD_enlM_1004004'
REG_PASSWORD = 'vniqedjjt2i8gcescopkcjrjrq'

#Nour Token
# REG_USERNAME = 'UPENN_OD_enlN_1004005'
# REG_PASSWORD = '7aodpm9op7s2jbjq693hc2ubkp'

r = Registrar(REG_USERNAME, REG_PASSWORD)
query_str = 'Select code from Course;'
courses = db.doQueryResults(conn,query_str)
num_insertions = 0

for course in courses:
    split = course[0].split("-")
    dept = split[0]
    c_num = split[1]
    #s_num = '001'
    query_str = "select sid from Section where sid like '{0}%';".format(course[0])
    sections =db.doQueryResults(conn,query_str)
    if sections is None:
        continue
    last = ''
    for section in sections:
        split = section[0].split("-")
        s_num = split[2]
        sec_code = split[0]+"-"+split[1]+"-"+split[2]
        if (sec_code == last):
            print ('skipping duplicate: ' + sec_code)
            continue
        else:
            last = sec_code
        query_str = "Select * from CourseListing where secid='{0}';".format(sec_code)
        res = db.doQueryResults(conn, query_str)
        if res is not None:
            continue # this section has an entry already
        try:
            print sec_code
            listing = r.section(dept, c_num, s_num)
            if listing is None:
                print ('SKIP ~ NO RESULT')
                continue;
            else:
                for meeting in listing["meetings"]:
                    start_time = meeting["start_time_24"]
                    end_time = meeting["end_time_24"]
                    meeting_days = meeting["meeting_days"]
                    term = meeting["term"]
                    query_str = "insert into CourseListing(secid,semid,start_time,end_time,days) values('{0}','{1}',{2},{3},'{4}');".format(sec_code,term,start_time,end_time,meeting_days)
                    print query_str
                    num_insertions = num_insertions + 1
                    db.doQuery(conn,query_str)
        except ValueError:
            print "Course section not found: %s-%s-%s" % (dept, c_num, s_num)

db.close(conn)
print 'Inserted: ' + str(num_insertions) + ' records'
