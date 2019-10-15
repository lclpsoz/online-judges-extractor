import json
import requests
from tqdm import tqdm

class userData:
	# Initialize all attributes, loading from
	# files when possible.
	def __init__ (self, folder):
		self.users = {}
		self.akas = {}
		self.folder = folder
		try:
			with open (folder + "users.json", 'r') as usersFile:
				self.users = json.load (usersFile)
			print ("users.json loaded!")
		except EnvironmentError:
			print ("users.json don't exist on this folder!")
			print ("Loading users information from usersRatedListLastMonth.json!")
			try:
				with open (folder + "usersRatedListLastMonth.json", 'r') as usersRatedListFile:
					usersRatedListLastMonth = json.load (usersRatedListFile)['result']
					for row in usersRatedListLastMonth:
						handle = row['handle'].lower()
						row.pop ('handle')
						self.users[handle] = row
				print ("Users loaded from usersRatedListLastMonth.json!")
			except EnvironmentError:
				print ("usersRatedListLastMonth.json don't exist on this folder!")
		
		try:
			with open (folder + "akas.json", 'r') as akasFile:
				self.akas = json.load (akasFile)
			print ("akas.json loaded!")
		except EnvironmentError:
			print ("akas.json don't exist on this folder!")
	
	# Receive handle. Return current handle of
	# the user.
	def getHandle (self, handle):
		print ("  Trying to get new handle!")
		if not handle in self.akas:
			self.akas[handle] = requests.get ("https://codeforces.com/profile/" + handle).url.split('/')[-1].lower()
			print ("  New handle: " + self.akas[handle])
			with open (self.folder + "akas.json", 'w') as akasFile:
				json.dump (self.akas, akasFile)
			
		return self.akas[handle]

	# Receive list of handles. Returns list of
	# users information on the same order of
	# the list of handles.
	def getUsers (self, handles):
		webPage = "https://codeforces.com/api/user.info?handles="
		for hand in handles:
			webPage += hand + ';'
		response = requests.get (webPage)
		users = json.loads (response.text)
		if (users['status'] == 'FAILED'):
			failHandle = self.getHandle (users['comment'].split(' ')[-3]).lower()
			print ("Failed on handle " + failHandle)
			for i in range (len (handles)):
				if (handles[i] == failHandle):
					handles[i] = self.getHandle (failHandle)
					print ("Change of handle: " + failHandle + " -> " + handles[i])

			self.getUsers (handles)
		else:
			for user in users['result']:
				handle = user.pop ('handle').lower()
				self.users[handle] = user
			with open (self.folder + "users.json", 'w') as usersFile:
				json.dump (self.users, usersFile)
	
	# Receive list lst and integer n. Returns a
	# list of lists, the lst splitted in lists
	# of a maximum length n, in the same order.
	@staticmethod
	def splitLst (lst, n):
		ret = []
		ax = []
		for i in range (len (lst)):
			ax.append (lst[i])
			if ((i+1)%n == 0):
				ret.append (ax)
				ax = []
		if (len (ax) > 0):
			ret.append (ax)
		
		return ret

	# Receive list of handles and list of information that
	# must be returned. Return the list of info in the same
	# order as the handles. If the info is not available,
	# "NO INFO" is placed in it field.
	def userInfo (self, allHandles, infos):
		unknowUsers = []
		for i in range (len (allHandles)):
			allHandles[i] = allHandles[i].lower()
			if (allHandles[i] in self.akas):
				allHandles[i] = self.getHandle (allHandles[i])
			if (not allHandles[i] in self.users):
				unknowUsers.append (allHandles[i])
		print (str (len (unknowUsers)) + " unknow users to process!")
		if (len (unknowUsers) > 0):
			print ("Thoses handles will be dividle in groups of 500 to be requested.")
			lstHandles = self.splitLst (unknowUsers, 500)
			for i in tqdm (range (len (lstHandles))):
				handles = lstHandles[i]
				self.getUsers (handles)
		
		var = []
		for handle in allHandles:
			var.append ([])
			for info in infos:
				if info in self.users[handle]:
					var[-1].append (self.users[handle][info])
				else:
					var[-1].append ("NO INFO")
					
		print ("Info from all " + str (len (allHandles)) + " handles obtained!")
		return var