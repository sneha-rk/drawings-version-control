# importing the requests library
import requests
 
# api-endpoint
URL = "http://127.0.0.1:8000/api/"
uid = 'admin'
pwd = 'LB5QUG3MzA'
 
# Returns all documents
# r = requests.get(url = 'http://139.59.22.126:80/api/'+ 'documents/documents/')
r = requests.get(url = URL + 'document_types/')

# print r
data = r.json()
print data

# Return all document types
# r1 = requests.get(url = URL + 'document_types/')
# data = r1.json()
# print data

# Add all document types
params = {
    u'label': ""
}

type_list = ['Preliminary', 'Tender', 'GFC', 'Sketch/Site Instruction', 'Shop Drawings', 'As Built']

for t in type_list:
	params = {
    u'label': t,
    "delete_time_period": None,
    "delete_time_unit": None,
    "trash_time_period": None,
    "trash_time_unit": None
	}
	print params
	r = requests.post(url = URL + 'document_types/', data=params, auth=(uid, pwd))
	print r
	data = r.json()
	print data