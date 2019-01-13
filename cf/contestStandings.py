import json
import requests
import os.path
from tabulate import tabulate
from userData import userData
from abbreviations import abbrev

# Needs "true" or "false" at the end and contests ID in the middle
pageStanding = ["https://codeforces.com/api/contest.standings?contestId=", "&from=1&count=15000&showUnofficial="]

contestId = input ("What is the contest id? ")
showUnofficial = input ("Show unofficial participants? (Y/N) ")
country = input ("Which country must filter the standings? ")

if (showUnofficial.lower () == "y"):
	pageStanding[1] += "true"
else:
	pageStanding[1] += "false"

if (not os.path.isfile ("standing" + contestId + ".json")):
	print ("Requesting standing information...")
	response = requests.get (pageStanding[0] + contestId + pageStanding[1])
	with open ("standing" + contestId + ".json", "w") as writeFile:
		writeFile.write (response.text)

with open ("standing" + contestId + ".json", "r") as readFile:
	data = json.load (readFile)
	rows = data.get('result').get('rows')
	users = []
	standing = []
	standing.append (["#", "TOTAL P.", "POINTS", "HANDLE", "COUNTRY", "ORG"])
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
print ("Contest standing info loaded!")

uData = userData()
infos = uData.userInfo (users, ['country', 'organization'])
for i in range (1, len (standing)):
	for info in infos[i-1]:
		standing[i].append (info)


standingBrazil = []
standingBrazil.append (standing[0])
for i in range (1, len (standing)):
	row = standing[i]
	if (row[4] == country):
		standingBrazil.append (row)
		
org = []
for comp in standingBrazil:
	if (comp[0] != '#'):
		org.append (comp[5])
	
org = abbrev (org, "organization")

for i in range (1, len (standingBrazil)):
	standingBrazil[i][5] = org[standingBrazil[i][5]]

print ("__________________Brazilian standings___________________")
print (tabulate (standingBrazil, headers="firstrow", tablefmt='github'))