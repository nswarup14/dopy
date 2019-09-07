
import json

from urllib import *
from urllib.request import Request , urlopen
import httplib2
import googleapiclient.discovery as discovery
from oauth2client import file, client, tools
import numpy as np

import jsonread
import config

CLIENT_SECRET = jsonread.get_path()+'/creds/client_secret.json'
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

# Overwrite None values later
ssId = config.configurator().spreadSheetId
if '\n' in ssId:
	ssId = ssId[:-1]
_SPREADSHEETID = ssId

# Start OAuth to retrive credentials

def refresh_access_token():
	with open("credentials.storage","r") as read_file:
		read_content = read_file.read()
		json_content = json.loads(read_content)

		client_id = json_content["client_id"]
		client_secret = json_content["client_secret"]
		refresh_token = json_content["refresh_token"]

		request = Request(json_content["token_uri"],
			data = parse.urlencode({
				"grant_type": "refresh_token",
				"client_id": client_id,
				"client_secret": client_secret,
				"refresh_token": refresh_token

				}).encode("utf-8"),
			headers = {
			"Content-type": "application/x-www-form-urlencoded",
			"Accept": "application/json"
			})
		temp = urlopen(request).read()
		temp_content = temp.decode("utf-8")
		response = json.loads(temp_content)
		return response["access_token"]

def get_credentials(access_token):
	user_agent = None
	revoke_uri = "https://oauth2.googleapis.com/revoke"

	credentials = client.AccessTokenCredentials(access_token= access_token, user_agent=user_agent, revoke_uri = revoke_uri)
	return credentials

def send_data(service):
	""" Sample emthod to write data to a spreadsheet"""
	range_name = 'A1:B2'
	values = [['1','2'],['3','4']]
	body = {
			'values': values
	}
	result = service.spreadsheets().values().update(spreadsheetId= _SPREADSHEETID, range=range_name, body=body, valueInputOption= "RAW").execute()

def read_data(service):
	""" Sample data to read data from a spreadsheet """
	# Figure how to include the sheet name
	range_name = 'A1:B2'
	result = service.spreadsheets().values().get(spreadsheetId= _SPREADSHEETID, range=range_name).execute()
	values = result.get('values',[])

def authorize_credentials():
	""" Fetch credentials from storage """
	credentials = file.Storage('credentials.storage').get()

	# If credentials dont exist in place then run the flow
	if credentials is None or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET, scope= SCOPE)
		http = httplib2.Http()
		credentials = tools.run_flow(flow, file.Storage('credentials.storage'), http=http)
	return credentials

def get_service(credentials):
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = discovery.build("sheets","v4",http)
	return service

def get_json_from(service):
	json_data = jsonread.convert_to_json()
	range_name ='A:C'
	result = service.spreadsheets().values().get(spreadsheetId= _SPREADSHEETID, range= range_name).execute()
	result_data = result.get('values',[])

	for each_entry in json_data:
		result_data = np.array(result_data)
		# How to handle empty sheets?
		all_ids = result_data[:,0]
		ID = each_entry["ID"]
		if ID in all_ids:
			index = all_ids.tolist().index(ID)
			items_of_ID = result_data[index,1]
			new_items_of_ID, new_cost = arrange_items(items_of_ID, each_entry["Clothes"], each_entry["Rest"])
			result_data = result_data.tolist()
			result_data[index][1] = new_items_of_ID
			temp_cost = int(result_data[index][2])
			temp_cost += new_cost
			result_data[index][2] = str(temp_cost)
		else:
			new_items_of_ID, new_cost = arrange_items(None, each_entry["Clothes"], each_entry["Rest"])
			new_entry = [ID, new_items_of_ID, new_cost]
			result_data = result_data.tolist()
			result_data.append(new_entry)

	result_data = np.array(result_data).tolist()
	body = {
		"values": result_data
	}
	print('result data ', result_data)
	result = service.spreadsheets().values().update(spreadsheetId= _SPREADSHEETID, body=body, range= 'A:C', valueInputOption ="RAW").execute()

def arrange_items(already_arranged, new_clothes, new_rest):
	delimiterOutside = '|'
	delimiterInside = '-'
	new_clothes.extend(new_rest)
	new_entries = new_clothes # Contains both
	if already_arranged is None:
		total_cost = 0
		already_arranged = []
		for each_entry in new_entries:
			new_item = each_entry.split(delimiterInside)
			if len(new_item) == 3:
				# Name, Quantity, Price
				# Rest Item
				if len(already_arranged) == 0:
					new_rest_entry = delimiterInside.join([new_item[0], new_item[1]])
					# Name, Quantity
					total_cost = total_cost + (int(new_item[2]) * int(new_item[1]))
					already_arranged.append(new_rest_entry)
				else:
					restFlag = 0
					for count in range(0, len(already_arranged)):
						split_added_already = already_arranged[count].split(delimiterInside)
						if len(split_added_already) == 2:
							if(new_item[0] == split_added_already[0]):
								split_added_already[1] = str(int(split_added_already[1]) + int(new_item[1]))
								total_cost = total_cost + int(new_item[1]) * int(new_item[2])
								already_arranged[count] = delimiterInside.join(split_added_already)
								restFlag = 1
								break
					if restFlag == 0:
						latest_entry = [new_item[0], new_item[1]]
						latest_entry = delimiterInside.join(latest_entry)
						total_cost = total_cost + (int(new_item[2]) * int(new_item[1]))
						already_arranged.append(latest_entry)
			elif len(new_item) == 4:
				# Name, Size, Color, Price
				# Clothes Item
				if len(already_arranged) == 0:
					new_clothes_entry = delimiterInside.join([new_item[0], new_item[1], new_item[2], '1'])
					# Name, Size, Color, Quantity
					total_cost = total_cost + int(new_item[3])
					already_arranged.append(new_clothes_entry)
				else:
					clothesFlag = 0
					for count in range(0, len(already_arranged)):
						split_added_already = already_arranged[count].split(delimiterInside)
						if len(split_added_already) == 4:
							if(new_item[0] == split_added_already[0] and new_item[1] == split_added_already[1] and new_item[2] == split_added_already[2]):
									split_added_already[3] = str(int(split_added_already[3]) + 1)
									total_cost = total_cost + int(new_item[3])
									already_arranged[count] = delimiterInside.join(split_added_already)
									clothesFlag = 1
									break
					if clothesFlag == 0:
						latest_entry = [new_item[0], new_item[1], new_item[2], "1"]
						latest_entry = delimiterInside.join(latest_entry)
						total_cost += int(new_item[3])
						already_arranged.append(latest_entry)
	else:
		already_arranged = already_arranged.split(delimiterOutside)
		total_cost = 0
		for each_entry in new_entries:
			new_item = each_entry.split(delimiterInside)
			flag = 0
			for count in range(0, len(already_arranged)):
				split_added_already = already_arranged[count].split(delimiterInside)
				if len(new_item) == 3 and len(split_added_already) == 2:
					if(new_item[0] == split_added_already[0]):
						split_added_already[1] = str(int(split_added_already[1]) + int(new_item[1]))
						total_cost = total_cost + int(new_item[1]) * int(new_item[2])
						already_arranged[count] = delimiterInside.join(split_added_already)
						flag = 1
						break
				elif len(new_item) == len(split_added_already) == 4:
					if(new_item[0] == split_added_already[0] and new_item[1] == split_added_already[1] and new_item[2] == split_added_already[2]):
						split_added_already[3] = str(int(split_added_already[3]) + 1)
						total_cost = total_cost + int(new_item[3])
						already_arranged[count] = delimiterInside.join(split_added_already)
						flag = 1
						break
			if flag == 0:
				if len(new_item) == 4:
					latest_entry = [new_item[0], new_item[1], new_item[2], '1']
					latest_entry = delimiterInside.join(latest_entry)
					total_cost += int(new_item[3])
					already_arranged.append(latest_entry)
				elif len(new_item) == 2:
					latest_entry = [new_item[0], new_item[1]]
					latest_entry = delimiterInside.join(latest_entry)
					total_cost = total_cost + (int(new_item[2]) * int(new_item[1]))
					already_arranged.append(latest_entry)
	return delimiterOutside.join(already_arranged), total_cost

def syncDB():
	try:
		credentials = authorize_credentials()
		credentials = file.Storage('credentials.storage').get()
	except :
		access_token = refresh_access_token()
		credentials = get_credentials(access_token)
	service = get_service(credentials)
	get_json_from(service)
	return 0
