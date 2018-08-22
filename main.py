import requests

url = "https://ctftime.org/event/list/upcoming"

def getWebpageData(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    return requests.get(url, headers=headers).text

def sendEmail():
    pass

data = getWebpageData(url)

table_start = '<table class="table table-striped">'
table_end = '</table>'

data = data[data.index(table_start):]
data = data[:data.index(table_end)+len(table_end)]

# Loop through each <tr> and parse --> Remove from data
