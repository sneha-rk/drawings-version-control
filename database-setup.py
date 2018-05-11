# importing the requests library
import requests
 
# api-endpoint
URL = "http://127.0.0.1:8000/api/"
uid = 'admin'
pwd = 'LB5QUG3MzA'
 
# Returns all documents
r = requests.get(url = 'http://139.59.22.126:80/api/'+ 'documents/documents/')
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
    u'label': "",
    "delete_time_period": "",
    "delete_time_unit": "",
    "trash_time_period": "",
    "trash_time_unit": ""
	}
type_list = ['Preliminary', 'Tender', 'GFC', 'Sketch/Site Instruction', 'Shop Drawings', 'As Built']

for t in type_list:
	params['label'] = t
	# print params
	r = requests.post(url = URL + 'document_types/', data=params, auth=(uid, pwd))
	# print r
	data = r.json()
	# print data


# Add all metadata types
params = {
    "default": "",
    "label": "",
    "lookup": "",
    "name": "",
    "parser": "",
    "validation": ""
}
labels = ['ID', 'IITH LR', 'Transmittal Reference', 'Architect', \
 'Building', 'Type', 'Services', 'Drawing No.', 'Drawing Title', \
 'Remarks']
name = ['id', 'iith-lr', 'transmittal-reference', 'architect', \
  'building', 'type', 'services', 'drawing-no', 'drawing-title', \
  'remarks']

for i, t in enumerate(labels):
	params['label'] = t
	params['name'] = name[i]

	if name[i] == 'transmittal-reference':
		params['parsers'] = 'metadata.parsers.DateAndTimeParser'
		params['validators'] = 'metadata.validators.DateAndTimeParser'
	# print params
	r = requests.post(url = URL + 'metadata_types/', data=params, auth=(uid, pwd))
	# print r
	data = r.json()
	# print data



# Add all metadata to document types

# Get all document labels
# Returns all documents
r = requests.get(url = URL + 'document_types/', auth=(uid, pwd))

# print r
data = r.json()
# print data

doc_types = []
for d in data['results']:
	doc_types.append(d['id'])
print doc_types


# Returns all metadata types
r = requests.get(url = URL + 'metadata_types/', auth=(uid, pwd))

# print r
data = r.json()
# print data

metadata = []
req = []
for d in data['results']:
	metadata.append(d['id'])
	# print d
	if d['label'] == 'Services' or  d['label'] == 'Remarks':
		req.append(False)
	else:
		req.append(True)
print metadata


params = {
    "metadata_type_pk": "",
    # "required": False
}
# Add all metadata to all document types
for t in doc_types:
	print t
	for i, m in enumerate(metadata):
			params['metadata_type_pk'] = m
			params['required'] = req[i]
			print params
			print  URL + 'document_types/' + str(t) +'/metadata_types'
			r = requests.post(url = URL + 'document_types/' + str(t) +'/metadata_types', data=params, auth=(uid, pwd))
			print r
			data = r.json()

# Create smart links























