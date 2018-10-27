import json
import os
import pprint
_path= os.path.abspath(os.curdir)


def get_path():
	return _path

def read_json():

	delimiter= '}'

	json_path= _path+'/data-entries.txt'
	with open(json_path,"r") as read_only_file:
		read_only_content= read_only_file.read()

		json_strings= read_only_content.split("}")
		json_strings.pop()
		#print(len(json_strings))
		for count in range(0,len(json_strings)):
			#print(json_strings[count])
			json_strings[count]= json_strings[count]+delimiter
			
	return json_strings

def convert_to_json():
	json_strings= read_json()
	actual_json=[]
	#print(len(json_strings))

	for count in range(0,len(json_strings)):
		actual_json.append(json.loads(json_strings[count]))
	"""	
	pp= pprint.PrettyPrinter(indent=4)
	pp.pprint(actual_json)
	"""
	return actual_json

if __name__=='__main__':
	actual_json= convert_to_json()
	pprint= pprint.PrettyPrinter(indent=4)
	pprint.pprint(actual_json)
	