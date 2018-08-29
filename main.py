import requests, pickle, datetime, os.path, smtplib

url = "https://ctftime.org/event/list/upcoming"
today = datetime.date.today()
months = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "June":6,
          "July":7, "Aug":8, "Sept":9, "Oct":10, "Nov":11, "Dec":12}
distance = 7

contestFile = 'past_contest_data'
pastContests = []
if os.path.exists(contestFile):
    pastContests = pickle.load(open(contestFile, "rb"))
maxContestLength = 20

def getWebpageData(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    return requests.get(url, headers=headers).text

def isSoon(date):
    if (date - today).days < distance:
        return True
    else:
        return False


# Turn on/off https://myaccount.google.com/lesssecureapps
def sendEmail(name, date, email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    password = input("Password: ")
    server.login("alexdejong737@gmail.com", password)
    msg = "YOUR MESSAGE!"
    server.sendmail("alexdejong737@gmail.com", "syedaliakrampervaiz@gmail.com", msg)
    server.quit()





data = getWebpageData(url)

table_start = '<table class="table table-striped"><tr><th>Name</th><th>Date</th><th>Format</th><th>Location</th><th>Weight</th><th colspan="2">Notes</th></tr>'
table_end = '</table>'

data = data[data.index(table_start)+len(table_start):]
data = data[:data.index(table_end)] + "<tr>"

# Parse each row of HTML <tr>

datalist = []
while len(data) != 0:
    index = data.index("<tr>")
    datalist.append(data[:index])
    data = data[index+4:]
    
datalist = datalist[1:]

for i in range(len(datalist)):
    # Get important information
    data = datalist[i]
    data = data[data.index('">') + 2:]
    name = data[:data.index("</a")]
    data = data[data.index('</a></td><td>')+13:]
    date = data[:data.index('&mdash')]

    # Parse date string
    day = int(date.split(" ")[0])
    month = months[date.split(" ")[1][:-2]]
    date = datetime.date(datetime.date.today().year, month, day)

    # Send email
    if isSoon(date) and name not in pastContests:
        sendEmail(name, date, "alexdejong737@gmail.com")
        #pastContests.append(name)
        print(name)
        if len(pastContests) > maxContestLength:
            pastContests = pastContests[1:]

pickle.dump(pastContests, open(contestFile, "wb+"))
