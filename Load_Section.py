import requests
import json
import re
import sys
import os
import db_functions as db
from APIRequest import get_request_pcr, print_components, set_http_pcr


conn = db.get_connection()
ratings_required = ["rDifficulty","rCourseQuality","rAmountLearned","rWorkRequired","rRecommendMajor","rRecommendNonMajor","rCommAbility","rInstructorAccess","rStimulateInterest","rInstructorQuality"]

filler = [-1] * len(ratings_required)
ratings = dict(zip(ratings_required, filler))

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
                query_str = "Select code from Alias where alias='{0}';".format(alias_list[0]);
                res = db.doQueryResults(conn,query_str)
		if res is None:
			print "Error: alias not found in table" 
		else:
			code = res[0]
                	http_str = set_http_pcr(course["path"])
			json_obj = get_request_pcr(http_str)
			courses_list_2 = json_obj["result"]["courses"]
			for course_2 in courses_list_2:
				path = course_2["path"] + "/sections"
				http_str = set_http_pcr(path)
				json_obj = get_request_pcr(http_str)
				sections_list = json_obj["result"]["values"]
				for section in sections_list:
					http_str = set_http_pcr(section["reviews"]["path"])
					json_obj = get_request_pcr(http_str)
					review_list = json_obj["result"]["values"]
					for review in review_list:
						print http_str
						semid = section["aliases"][0] + "-" + section["courses"]["semester"]
						if len(section["aliases"]) > 1:
							print section["aliases"]
						
						# loop to fill in any missing properties, saved as -1 if missing
						for r in ratings_required:
							try:
								ratings[r] = review["ratings"][r]
							except KeyError:
								ratings[r] = -1
						#print ratings
						query_str = """select * from Section where sid="{0}";""".format(semid)
						res = db.doQueryResults(conn,query_str)
						if res is not None:
							continue	# skip sections we have already added to avoid extra errors
						query_str = """insert into Section(difficulty,quality,num_students,meeting_days,time,sid,AmountLearned,WorkRequired,RecommendMajor,RecommendNonMajor,CommAbility,ProfAccess,num_reviews, StimInterest) values ({0},{1},{2},NULL,NULL,"{3}",{4},{5},{6},{7},{8},{9},{10},{11});""".format(ratings["rDifficulty"],ratings["rCourseQuality"],review["num_students"],semid ,ratings["rAmountLearned"],ratings["rWorkRequired"],ratings["rRecommendMajor"],ratings["rRecommendNonMajor"],ratings["rCommAbility"],ratings["rInstructorAccess"],review["num_reviewers"], ratings["rStimulateInterest"])	
						#print query_str
						db.doQuery(conn,query_str)				
						query_str = """insert into Teaches(sid,pid,InstructorQuality) values ("{0}","{1}",{2});""".format(semid,review["instructor"]["id"],ratings["rInstructorQuality"])
						#print query_str
						res = db.doQuery(conn,query_str)
						print semid
db.close(conn)
