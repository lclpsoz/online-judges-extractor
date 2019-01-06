import json
import requests
from tabulate import tabulate

def prob (probs):
	#print (probs[0].keys())
	return [int (p['points']) for p in probs]

def getHandle (handle):
	return requests.get ("https://codeforces.com/profile/" + handle).url.split('/')[-1]

def country (handle):
	response = requests.get ("https://codeforces.com/api/user.info?handles=" + handle)
	user = json.loads (response.text)
	if (user['status'] == 'FAILED'):
		handle = getHandle (handle)
		response = requests.get ("https://codeforces.com/api/user.info?handles=" + handle)
		user = json.loads (response.text)
	if 'country' in user['result'][0]:
		return user['result'][0]['country']
	else:
		return 'NO COUNTRY'

	
def getCountries (handles):
	webPage = "https://codeforces.com/api/user.info?handles="
	for hand in handles:
		webPage += hand + ';'
	response = requests.get (webPage)
	users = json.loads (response.text)
	if (users['status'] == 'FAILED'):
		#print (users['comment'])
		return users['comment'].split(' ')[-3]
	else:
		return users['result']
	
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
	#for i in ret:
		#print (len (i))
	
	return ret
			

def countries (allHandles):
	lstHandles = splitLst (allHandles)
	var = []
	qntFail = 0
	for handles in lstHandles:
		ret = getCountries (handles)
		while type (ret) == str:
			qntFail += 1
			failHandle = ret
			for i in range (len (handles)):
				if (handles[i] == failHandle):
					handles[i] = getHandle (failHandle)
					print ("Fail: " + failHandle + " -> " + handles[i])
			ret = getCountries (handles)
		for user in ret:
			if "country" in user:
				var.append (user['country'])
			else:
				var.append ("NO COUNTRY")
	print ("Qnt of changed Handles: " + str (qntFail))		
	return var

with open ("standing1099.json", "r") as readFile:
	
	data = json.load (readFile)
	rows = data.get('result').get('rows')
	print (rows[0].keys())
	users = []
	standing = []
	standing.append (["#", "TOTAL P.", "POINTS", "HANDLE", "COUNTRY"])
	for i in range (len (rows)):
		#print (str (i) + "/" + str (len(rows)-1))
		standing.append ([])
		now = rows[i]
		#print (now['rank'])
		i += 1
		#print (now)
		standing[i].append (now['rank'])
		standing[i].append (now['points'])
		standing[i].append (prob (now['problemResults']))
		standing[i].append (now['party']['members'][0]['handle'])
		users.append(now['party']['members'][0]['handle'])
		i -= 1
		#print (i['rank'], end=":\t")
		#print (int (i['points']), end='\t')
		#print (prob (i['problemResults']))
		#print (i['party']['members'][0]['handle'], end = '\t')
		#print (country (i['party']['members'][0]['handle']))
	#print (users)
print ("FILE PROCESSED!!!!!")
count = countries (users)
for i in range (1, len (standing)):
	standing[i].append (count[i-1])

standingBrazil = []
standingBrazil.append (standing[0])
for row in standing:
	if (row[4] == 'Brazil'):
		standingBrazil.append (row)

print (standing)
print (tabulate (standing, headers="firstrow", tablefmt='github'))
print ("________________________________________________________")
print ("________________________________________________________")
print ("________________________________________________________")
print (tabulate (standingBrazil, headers="firstrow", tablefmt='github'))