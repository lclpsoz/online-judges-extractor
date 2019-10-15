import json
import requests
import os.path
from tabulate import tabulate
from userData import userData
from abbreviations import abbrev
from generateHtml import generateHtml

# Needs "true" or "false" at the end and contests ID in the middle
pageStanding = ["https://codeforces.com/api/contest.standings?contestId=", "&from=1&count=15000&showUnofficial="]

headers = ["#", "TOTAL P.", "POINTS", "HANDLE", "COUNTRY", "ORG"]
folder = "files/"

contestId = input ("What is the contest id? ")
showUnofficial = input ("Show unofficial participants? (Y/N) ")
country = input ("Which country must filter the standings (Global for no filter)? ")

flagShow = ""
if (showUnofficial.lower () == "y"):
	pageStanding[1] += "true"
	flagShow = "_unofficial"
else:
	pageStanding[1] += "false"
	flagShow = "_official"

standingFileName = folder + "standing" + contestId + flagShow + ".json"

if (not os.path.isfile (standingFileName)):
	print ("Requesting standing information...")
	response = requests.get (pageStanding[0] + contestId + pageStanding[1])
	with open (standingFileName, "w") as writeFile:
		writeFile.write (response.text)

with open (standingFileName, "r") as readFile:
	data = json.load (readFile)
	rows = data.get('result').get('rows')
	users = []
	standing = []
	standing.append (headers)
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

uData = userData(folder)
infos = uData.userInfo (users, ['country', 'organization'])
for i in range (1, len (standing)):
	for info in infos[i-1]:
		standing[i].append (info)


standingFiltered = []
standingFiltered.append (standing[0])
for i in range (1, len (standing)):
	row = standing[i]
	if (country == 'Global' or row[4] == country):
		standingFiltered.append (row)
		
org = []
for comp in standingFiltered:
	if (comp[0] != '#'):
		org.append (comp[5])
	
org = abbrev (org, "organization", folder)

for i in range (1, len (standingFiltered)):
	standingFiltered[i][5] = org[standingFiltered[i][5]]

print ("__________________Brazilian standings___________________")
print (tabulate (standingFiltered, headers="firstrow", tablefmt='github'))


filePathHtml = folder + "contest" + str (contestId) + flagShow + "_" + country + ".html"
generateHtml (filePathHtml,	headers, standingFiltered)