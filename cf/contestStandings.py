import json
import requests
from tabulate import tabulate
from userData import userData

with open ("standing1099.json", "r") as readFile:
	data = json.load (readFile)
	rows = data.get('result').get('rows')
	users = []
	standing = []
	standing.append (["#", "TOTAL P.", "POINTS", "HANDLE", "COUNTRY"])
	for i in range (len (rows)):
		standing.append ([])
		now = rows[i]
		
		i += 1
		standing[i].append (now['rank'])
		standing[i].append (now['points'])
		standing[i].append ([int (p['points']) for p in now['problemResults']])
		standing[i].append (now['party']['members'][0]['handle'])
		users.append(now['party']['members'][0]['handle'])
		i -= 1
		
print ("FILE PROCESSED!!!!!")
uData = userData()
count = uData.countries (users)
for i in range (1, len (standing)):
	standing[i].append (count[i-1])

standingBrazil = []
standingBrazil.append (standing[0])
for i in range (len (standing)):
	row = standing[i]
	if (row[4] == 'Brazil'):
		standingBrazil.append (row)

#print (standing)
#print (tabulate (standing, headers="firstrow", tablefmt='github'))
print ("__________________Brazilian standings___________________")
print (tabulate (standingBrazil, headers="firstrow", tablefmt='github'))