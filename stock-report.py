import argparse
import json
import os
import requests
import smtplib
import socket
import time

# Create delay for effect
time.sleep(5)

# variables and enumerate list
stockurl = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/jsonp?symbol="
gmpass = os.environ['gmpass']
gmuser = os.environ['gmuser']
l = []

# get host name (container id)
h = socket.gethostname()

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--symbols', help="Stock symbols to search.")
parser.add_argument('--email', help="Email address for report.")
args = parser.parse_args()
symbols = args.symbols.split(';')
email = args.email
print(email)
print(symbols)

# get stock quote and populate list
for symbol in symbols:
    r = requests.get(stockurl + symbol)
    print(r.text)
    s = json.loads(r.text[18:-1])
    price = (s['LastPrice'])
    l.append(symbol + ' = ' + str(s['LastPrice']) + '\n')  

# send email
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(gmuser,gmpass)
header = 'To:' + email  + '\n' + 'From: ' + gmuser + '\n' + 'Subject:' + h + '\n'
msg = header + ''.join(l)
smtpserver.sendmail(gmuser, email, msg)
smtpserver.close()
