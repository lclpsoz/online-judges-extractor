
def generateHtml (filePath, headers, table):
    with open (filePath, "w") as f:
        html = """<html><table border="1">"""
        for h in headers:
            html += "<th>" + h + "</th>"
        html += "</tr>"
        for line in table:
            if (line[0] == "#"):
                continue
            html += "<tr>"
            for i in range (len (line)):
                html += "<td>"
                if (headers[i] == "HANDLE"):
                    html += '<a href="https://codeforces.com/profile/' + line[i] + '">' + str (line[i]) + '</a>'
                elif (headers[i] == "PROBLEM"):
                    contestId = str (line[i][0])
                    problemIndex = str (line[i][1])
                    problemName =  contestId + problemIndex
                    html += '<a href="https://codeforces.com/contest/' + contestId + '/problem/' + problemIndex + '">' + problemName + '</a>'
                else:
                    html += str (line[i])
                html += "</td>"
            html += "</tr>"
        html += "</table></html>"
        f.write (html)