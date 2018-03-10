import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr
conn = db.get_connection()
last_checked = ''
query_str = 'Select sid from Section;'
courses = db.doQueryResults(conn,query_str)
for course in courses:
    split = course[0].split("-")
    c_num_w_section = split[0]+"-"+split[1]+"-"+split[2]
    if (last_checked == c_num_w_section):
        continue
    else:
        last_checked = c_num_w_section
    #find all semesters for that section
    query_str_sections = "select * from Section where sid like '{0}%';".format(c_num_w_section)
    sections =db.doQueryResults(conn,query_str_sections)
    #find how many there are of them
    query_str_num = "select count(*) from Section where sid like '{0}%';".format(c_num_w_section)
    num_section_instances =db.doQueryResults(conn,query_str_num)
    if sections is None:
        continue
    avg_diff = 0.0
    avg_qual = 0.0
    avg_num_stud = 0.0
    avg_wk_reqd = 0.0
    avg_rec_maj = 0.0
    avg_rec_nomaj = 0.0
    avg_com_ability = 0.0
    avg_pf_access = 0.0
    avg_num_rev = 0.0
    avg_stim_int = 0.0

    for section in sections:
        #do addition
        avg_diff += float(section[0])
        avg_qual += float(section[1])
        avg_num_stud += float(section[2])
        avg_wk_reqd += float(section[6])
        avg_rec_maj += float(section[7])
        avg_rec_nomaj += float(section[8])
        avg_com_ability += float(section[9])
        avg_pf_access += float(section[10])
        avg_num_rev += float(section[11])
        avg_stim_int += float(section[12])

    query_str_teaches = "select * from Teaches where sid like '{0}%';".format(c_num_w_section)
    teaches =db.doQueryResults(conn,query_str_teaches)
    #find how many there are of them
    query_str_num_teaches = "select count(*) from Teaches where sid like '{0}%';".format(c_num_w_section)
    num_teaches_instances =db.doQueryResults(conn,query_str_num_teaches)
    if teaches is None:
        continue
    avg_pf_qual = 0.0
    for teach in teaches:
        #do addition
        avg_pf_qual += float(teach[2])

    #do division
    avg_diff = avg_diff/float((num_section_instances[0])[0])
    avg_qual = avg_qual/float((num_section_instances[0])[0])
    avg_num_stud = avg_num_stud/float((num_section_instances[0])[0])
    avg_wk_reqd = avg_wk_reqd/float((num_section_instances[0])[0])
    avg_rec_maj = avg_rec_maj/float((num_section_instances[0])[0])
    avg_rec_nomaj = avg_rec_nomaj/float((num_section_instances[0])[0])
    avg_com_ability = avg_com_ability/float((num_section_instances[0])[0])
    avg_pf_access = avg_pf_access/float((num_section_instances[0])[0])
    avg_num_rev = avg_num_rev/float((num_section_instances[0])[0])
    avg_stim_int = avg_stim_int/float((num_section_instances[0])[0])
    avg_pf_qual = avg_pf_qual/float((num_teaches_instances[0])[0])

    query_update_avg = "insert into SectionAverages(secid,difficulty,quality,num_students,work_required,rec_major,rec_non_major,comm_ability,prof_access,num_reviews,stim_interest,instruct_quality) values('{0}','{1}',{2},{3},'{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}');".format(c_num_w_section,avg_diff,avg_qual,avg_num_stud,avg_wk_reqd,avg_rec_maj,avg_rec_nomaj,avg_com_ability,avg_pf_access,avg_num_rev,avg_stim_int,avg_pf_qual)
    print query_update_avg
    db.doQuery(conn,query_update_avg)

db.close(conn)
