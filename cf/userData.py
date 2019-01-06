import json
import requests
from tqdm import tqdm

class userData:
	def __init__ (self):
		self.users = {}
		self.akas = {}
		try:
			with open ("users.json", 'r') as usersFile:
				self.users = json.load (usersFile)
			print ("users.json loaded!")
		except EnvironmentError:
			print ("users.json don't exist on this folder!")
			print ("Loading users information from usersRatedListLastMonth.json!")
			try:
				with open ("usersRatedListLastMonth.json", 'r') as usersRatedListFile:
					usersRatedListLastMonth = json.load (usersRatedListFile)['result']
					for row in usersRatedListLastMonth:
						handle = row['handle'].lower()
						row.pop ('handle')
						self.users[handle] = row
				print ("Users loaded from usersRatedListLastMonth.json!")
			except EnvironmentError:
				print ("usersRatedListLastMonth.json don't exist on this folder!")
		
		try:
			with open ("akas.json", 'r') as akasFile:
				self.akas = json.load (akasFile)
			print ("akas.json loaded!")
		except EnvironmentError:
			print ("akas.json don't exist on this folder!")
		
	def getHandle (self, handle):
		if handle in self.akas:
			info = self.akas[handle]
			self.akas.pop (handle)
			self.akas[handle] = info
			return self.akas[handle]
		else:
			self.akas[handle] = requests.get ("https://codeforces.com/profile/" + handle).url.split('/')[-1]
			with open ("akas.json", 'w') as akasFile:
				json.dump (self.akas, akasFile)
			
			return self.akas[handle]

	def country (self, handle):
		response = requests.get ("https://codeforces.com/api/user.info?handles=" + handle)
		user = json.loads (response.text)
		if (user['status'] == 'FAILED'):
			handle = self.getHandle (handle)
			response = requests.get ("https://codeforces.com/api/user.info?handles=" + handle)
			user = json.loads (response.text)
		if 'country' in user['result'][0]:
			return user['result'][0]['country']
		else:
			return 'NO COUNTRY'

	@staticmethod
	def getUsers (handles):
		webPage = "https://codeforces.com/api/user.info?handles="
		for hand in handles:
			webPage += hand + ';'
		response = requests.get (webPage)
		users = json.loads (response.text)
		if (users['status'] == 'FAILED'):
			return users['comment'].split(' ')[-3]
		else:
			return users['result']
	
	@staticmethod
	def splitLst (lst):
		ret = []
		ax = []
		for i in range (len (lst)):
			ax.append (lst[i])
			if ((i+1)%500 == 0):
				ret.append (ax)
				ax = []
		if (len (ax) > 0):
			ret.append (ax)
		
		return ret

	def countries (self, allHandles):
		unknowUsers = []
		for i in range (len (allHandles)):
			allHandles[i] = allHandles[i].lower()
			if (allHandles[i] in self.akas):
				#print ("Known Fail: " + allHandles[i] + " -> " + self.akas[allHandles[i]])
				allHandles[i] = self.getHandle (allHandles[i])
			if (not allHandles[i] in self.users):
				unknowUsers.append (allHandles[i])
		print (unknowUsers)
		lstHandles = self.splitLst (unknowUsers)
		qntFail = 0
		for i in tqdm (range (len (lstHandles))):
			handles = lstHandles[i]
			#print ("Processing Chuncks of Handles... " + str (i) + "/" + str (len (lstHandles)), end='\r') 
			ret = self.getUsers (handles)
			while type (ret) == str:
				qntFail += 1
				failHandle = ret.lower()
				for i in range (len (handles)):
					if (handles[i] == failHandle):
						handles[i] = self.getHandle (failHandle).lower()
						print ("Fail: " + failHandle + " -> " + handles[i])
				ret = self.getUsers (handles)
			for user in ret:
				handle = user['handle'].lower()
				#print (handle)
				user.pop ('handle')
				self.users[handle] = user
		print ("Qnt of NEW changed Handles: " + str (qntFail))
		
		var = []
		for handle in allHandles:
			#print (handle)
			#print (self.users[handle])
			if "country" in self.users[handle]:
				var.append (self.users[handle]['country'])
			else:
				var.append ("NO COUNTRY")
					
		print ("Countries from all " + str (len (allHandles)) + " handles obtained!")
		return var

