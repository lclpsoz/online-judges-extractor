# Obtain the list of problems to be done by a specific
# user based on previous contests done in a specified year.
# Ordered by rating of the problem.

import json
import requests
import datetime as dt
from tqdm import tqdm
from generateHtml import generateHtml
from datetime import datetime
from time import time

# Get standing info from CODEFORCES without
# standing.
def requestContestInfo (contestId):
    pageStanding = ['https://codeforces.com/api/contest.standings?contestId=', '&from=1&count=1&showUnofficial=true']
    pageNow = pageStanding[0] + str(contestId) + pageStanding[1]
    info = json.loads (requests.get (pageNow).text)
    del (info['result']['rows'])
    return info


user = input ("Username: ")
year = input ("Year: (Integer OR all) ")
showRating = input ("Show rating of the problem? (Y OR N) ")
reqNumSubmissions = 10000

delta = 1
if (year.lower() == "all"):
    year = 2000
    delta = 50

startYear = dt.datetime (int (year), 1, 1)
startNextYear = dt.datetime ((int(year)+delta), 1, 1)

print ("Requesting the " + str (reqNumSubmissions) + " latests submissions from " + user + ".")
pageUserSubmissions = "https://codeforces.com/api/user.status?handle=" + user + "&from=1&count=" + str (reqNumSubmissions)
userSubmissions = json.loads (requests.get (pageUserSubmissions).text).get('result')

print ("Requesting contest list.")
pageContests = "https://codeforces.com/api/contest.list?gym=false"
contests = json.loads (requests.get (pageContests).text).get('result')
# print (contests[0])
# start = dt.datetime.fromtimestamp (contests[0]['startTimeSeconds'])
# print (start.timestamp())
# print (start.isoformat())
# print (startYear.isoformat())
# print (startNextYear.isoformat())

contestsIdsThisYear = {}
for contest in contests:
    start = dt.datetime.fromtimestamp (contest['startTimeSeconds'])
    if (contest['phase'] == 'FINISHED' and start >= startYear and start < startNextYear):
        contestsIdsThisYear[contest['id']] = contest['name']

contestsIdThisYearWithUser = set()
contestsFails = []
problems_solved = set()
for sub in userSubmissions:
    contestId = sub['contestId'] 
    if contestId in contestsIdsThisYear:
        contestsIdThisYearWithUser.add(contestId)
        problems_solved.add(str(contestId) + sub['problem']['index'])


opt = 0

user_unsolved_problems = []
# Solution based on PROBLEMSET
if(opt == 0):
    problemset_url = 'https://codeforces.com/api/problemset.problems'
    problemset = json.loads (requests.get (problemset_url).text).get('result')

    for i in range(len(problemset['problems'])):
        pb = problemset['problems'][i]
        pb_stats = problemset['problemStatistics'][i]
        pb_id = str(pb['contestId']) + str(pb['index'])
        if pb['contestId'] > 885 and pb['contestId'] in contestsIdThisYearWithUser and pb_id not in problems_solved:
            user_unsolved_problems.append((pb['contestId'], pb['index'], pb['name'], pb_stats['solvedCount']))


else:
    # Solution based on CONTEST

    contestsIdThisYearWithUser = list (contestsIdThisYearWithUser)
    contestsThisYearWithUser = []
    print ("Requesting contests info.")
    for i in tqdm (range (len (contestsIdThisYearWithUser))):
        contestStandingJson = requestContestInfo (contestsIdThisYearWithUser[i])
        contestStanding = contestStandingJson.get('result')
        contestsThisYearWithUser.append (contestStanding)

    userSolvedProblemsPerContest = {}
    for sub in userSubmissions:
        contestId = sub['contestId'] 
        if (contestId in contestsIdsThisYear and sub['verdict'] == 'OK'):
            if (not contestId in userSolvedProblemsPerContest):
                userSolvedProblemsPerContest[contestId] = set ()   
            userSolvedProblemsPerContest[contestId].add (sub['problem']['index'])

    for contest in contestsThisYearWithUser:
        contestId = contest['contest']['id']
        problems = contest['problems']
        if (contestId in userSolvedProblemsPerContest):
            for problem in problems:
                if (not problem['index'] in userSolvedProblemsPerContest[contestId]):
                    problemRating = -1
                    if ('rating' in problem):
                        problemRating = problem['rating']
                    user_unsolved_problems.append ((contestId, problem['index'], problem['name'], problemRating))



headers = ['PROBLEM', 'PROBLEM NAME']
if opt == 0:
    user_unsolved_problems.sort (key=lambda tup: -tup[3])
    headers.append('SOLVED COUNT')
else:
    user_unsolved_problems.sort (key=lambda tup: tup[3])
    headers.append('RATING')

table = []
for p in user_unsolved_problems:
    table.append ([(p[0], p[1]), p[2]])
    if (showRating == 'Y'):
        if (p[3] == -1):
            table[-1].append ('UNAVAILABLE')
        else:
            table[-1].append (p[3])
    else:
        table[-1].append ('HIDDEN')

for l in table:
    print (l)

generateHtml ('files/upsolving_' + user + '_' + datetime.now().isoformat().split('.')[0] + '.html', headers, table)