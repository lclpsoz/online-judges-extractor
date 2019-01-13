import json
import os.path


def abbrev (names, field):
	fileName = "abbrev-" + field + ".json"
	abbrevNames = {}
	if (os.path.isfile (fileName)):
		with open (fileName, 'r') as abbrevFile:
			abbrevNames = json.load (abbrevFile)

	for name in names:
		aux = name
		if (aux in abbrevNames):
			aux = abbrevNames[aux]
		if (len (aux) > 10):
			aux = input("That abbreviation to use for '" + aux + "'? ")
		aux.strip()
		abbrevNames[name] = aux
	
	with open (fileName, 'w') as abbrevFile:
		json.dump (abbrevNames, abbrevFile)

	return abbrevNames