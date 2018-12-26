import googleapiclient.discovery as discovery
import json
import numpy as np

from urllib import *
from urllib.request import Request , urlopen

import httplib2
from oauth2client import file, client, tools
import jsonread

import config



CLIENT_SECRET= jsonread.get_path()+'/creds/client_secret.json'
SCOPE= 'https://www.googleapis.com/auth/spreadsheets'

# Overwrite None values later
ssId = config.configurator().spreadSheetId
if '\n' in ssId:
	ssId = ssId[:-1]
_SPREADSHEETID= ssId
_SHEETID= 0

_TOTAL= 4
# Start OAuth to retrive credentials

def refresh_access_token():
	with open("credentials.storage","r") as read_file:
		read_content= read_file.read()
		json_content= json.loads(read_content)

		client_id= json_content["client_id"]
		client_secret= json_content["client_secret"]
		refresh_token= json_content["refresh_token"]

		request= Request(json_content["token_uri"],
			data= parse.urlencode({
				"grant_type": "refresh_token",
				"client_id": client_id,
				"client_secret": client_secret,
				"refresh_token": refresh_token

				}).encode("utf-8"),
			headers= {
			"Content-type": "application/x-www-form-urlencoded",
			"Accept": "application/json"
			})
		temp= urlopen(request).read()
		temp_content= temp.decode("utf-8")
		response= json.loads(temp_content)
		print((jsonread.pprint.PrettyPrinter(indent=4)).pprint(response))
		return response["access_token"]

def get_credentials(access_token):
	user_agent = None
	revoke_uri = "https://oauth2.googleapis.com/revoke"

	credentials= client.AccessTokenCredentials(access_token= access_token, user_agent=user_agent, revoke_uri = revoke_uri)
	return credentials


def send_data(service):
	""" Sample emthod to write data to a spreadsheet"""
	range_name='A1:B2'
	values=[['1','2'],['3','4']]
	body={
			'values': values
			}
	result= service.spreadsheets().values().update(spreadsheetId= _SPREADSHEETID, range=range_name, body=body, valueInputOption= "RAW").execute()

	print("done job")


def read_data(service):
	""" Sample data to read data from a spreadsheet """
	# Figure how to include the sheet name
	range_name='A1:B2'

	result= service.spreadsheets().values().get(spreadsheetId= _SPREADSHEETID, range=range_name).execute()
	values=result.get('values',[])
	print('{0} is the values'.format(values))

def authorize_credentials():
	""" Fetch credentials from storage """
	credentials= file.Storage('credentials.storage').get()

	# If credentials dont exist in place then run the flow
	if credentials is None or credentials.invalid:
		flow= client.flow_from_clientsecrets(CLIENT_SECRET, scope= SCOPE)
		http= httplib2.Http()
		credentials= tools.run_flow(flow, file.Storage('credentials.storage'), http=http)

	return credentials


def get_service(credentials):
	http=httplib2.Http()
	http= credentials.authorize(http)
	service= discovery.build("sheets","v4",http)

	return service

def get_sheet_data():
	spreadsheetId= None
	sheetId= None
	path= jsonread.get_path()
	with open(path+"/sheet-id.json","r") as read_file:
		content= read_file.read()
		json_content= json.loads(content)

		spreadsheetId= json_content['spreadsheetId']
		sheetId= json_content['sheetId']

	return spreadsheetId,sheetId



def get_json_from(service):
	json_data= jsonread.convert_to_json()
	# Check this one please
	range_name='A:C'
	result= service.spreadsheets().values().get(spreadsheetId= _SPREADSHEETID, range= range_name ).execute()
	result_data= result.get('values',[])
	no_entries= len(result_data)
	#print(result)
	for each_entry in json_data:
		result_data= np.array(result_data)

		#print(result_data)
		# How to handle empty sheets?

		all_ids= result_data[:,0]
		ID= each_entry["ID"]
		print(ID)
		if ID in all_ids:
			#print(ID)
			index=all_ids.tolist().index(ID)

			items_of_ID= result_data[index,1]
			current_cost= result_data[index,2]
			#print(items_of_ID," ", current_cost)
			#print(items_of_ID)
			new_items_of_ID, new_cost= arrange_items(items_of_ID, each_entry[ID])
			#print(new_items_of_ID)
			#print(result_data[index,1])
			result_data=result_data.tolist()
			result_data[index][1]= new_items_of_ID ######## FUcking error is here

			#print(result_data[index][1])
			temp_cost= int(result_data[index][2])
			#print(type(result_data[index,2]))
			temp_cost+= new_cost
			result_data[index][2]= str(temp_cost)
			#print(result_data[index])

		else:

			new_entry=[]
			#print(each_entry[ID])
			new_items_of_ID, new_cost= arrange_items(None, each_entry[ID] )
			new_entry=[ID, new_items_of_ID, new_cost]
			result_data=result_data.tolist()
			result_data.append(new_entry)
			no_entries+=1

	result_data=np.array(result_data)
	result_data=result_data.tolist()
	"""
	for temp in range(0,len(result_data)):
		print(result_data[temp])
	"""
	body={
		"values": result_data
	}
	result= service.spreadsheets().values().update(spreadsheetId= _SPREADSHEETID, body
		=body, range= 'A:C', valueInputOption ="RAW").execute()

	print("Fucking job is done")

def arrange_items(already_arranged, new_entries):
	delimiterOutside= '|'
	delimiterInside= '-'

	if already_arranged is None:

		total_cost=0
		already_arranged=[]
		for each_entry in new_entries:
			item_split= each_entry.split(delimiterInside)

			if len(already_arranged)==0:
				latest_entry= [item_split[0],item_split[1], item_split[2], "1"]
				latest_entry= delimiterInside.join(latest_entry)

				total_cost+= int(item_split[3])
				already_arranged.append(latest_entry)
				#print(already_arranged)

			else:
				flag=0
				for count in range(0,len(already_arranged)):
					split_added_already= already_arranged[count].split(delimiterInside)
					if(item_split[0]==split_added_already[0] and item_split[1]==split_added_already[1] and split_added_already[2]== item_split[2]):
						split_added_already[3]=int(split_added_already[3])
						split_added_already[3]+=1
						split_added_already[3]=str(split_added_already[3])
						total_cost+=int(item_split[3])
						already_arranged[count]=delimiterInside.join(split_added_already)
						#print(already_arranged[count])
						flag=1
						#print(already_arranged)
						break

				if flag==0:
					latest_entry=[item_split[0],item_split[1], item_split[2], "1"]
					latest_entry= delimiterInside.join(latest_entry)
					total_cost+= int(item_split[3])
					already_arranged.append(latest_entry)
					#print(already_arranged)

		#print(delimiterOutside.join(already_arranged)," ", total_cost)
		return delimiterOutside.join(already_arranged), total_cost

	else:
		#print(already_arranged)
		already_arranged= already_arranged.split(delimiterOutside)
		#print(already_arranged)
		total_cost=0
		for each_entry in new_entries:
			item_split= each_entry.split(delimiterInside)
			flag=0
			for count in range(0,len(already_arranged)):
				#print(already_arranged[count])
				split_added_already= already_arranged[count].split(delimiterInside)
				#print(split_added_already)
				if(item_split[0]==split_added_already[0] and item_split[1]==split_added_already[1] and split_added_already[2]== item_split[2]):
					#print(split_added_already)
					split_added_already[3]=int(split_added_already[3])
					split_added_already[3]+=1
					split_added_already[3]=str(split_added_already[3])
					total_cost+=int(item_split[3])
					already_arranged[count]= delimiterInside.join(split_added_already)
					flag=1
					#print(already_arranged)
					break
			if flag==0:
				#print("Not entered")
				latest_entry= [item_split[0],item_split[1], item_split[2], "1"]
				latest_entry= delimiterInside.join(latest_entry)
				total_cost+= int(item_split[3])
				already_arranged.append(latest_entry)
		#print(delimiterOutside.join(already_arranged))
		#print(already_arranged)
		return delimiterOutside.join(already_arranged), total_cost

def syncDB():
	try:
		credentials= authorize_credentials()
		credentials= file.Storage('credentials.storage').get()
	except :
		access_token= refresh_access_token()
		credentials= get_credentials(access_token)
		## Check when token expires
		# print(credentials.read())
		# print(type(credentials))

	service= get_service(credentials)
	get_json_from(service)
	return 0