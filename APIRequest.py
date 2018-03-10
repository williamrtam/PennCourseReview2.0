import requests 
import json
import re
import sys
import os
#from penn import Registrar

#For Registrar Access
#AUTH_BEARER = 'UPENN_OD_enka_1003904'
#AUTH_TOKEN = '8enqh1mlsj4ed7oj3nvk44c84s'
#reg = Registrar(AUTH_BEARER, AUTH_TOKEN)




def get_request_pcr(which_request):
	try:
            response = requests.get(which_request)
            vals = json.loads(response.text)
            return vals #returns the JSON object
        except:
            return None

def print_components(json):
	for value in json:	
		print(json.items())


def set_http_pcr(query):
	url = 'http://api.penncoursereview.com/v1/'
	token = '?token=Dh48uOK66gkUcAS5tW6nCd_Uu02TaJ'

	overall = url + query + token
	return overall		

