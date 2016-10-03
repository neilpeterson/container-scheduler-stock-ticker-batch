import argparse
import json
import os
import requests
import smtplib
import socket
import time

# variables and enumerate list
stockurl = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/jsonp?symbol="
gmpass = os.environ['gmpass']
gmuser = os.environ['gmuser']
l = []

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--symbols', help="Stock symbols to search.")
parser.add_argument('--email', help="Email address for report.")
parser.add_argument('--delay', help="Delay in seconds for demo.")
args = parser.parse_args()
symbols = args.symbols.split(';')
email = args.email
delay = args.delay

# Create delay for effect
if delay:
    time.sleep(int(delay))

# get host name (container id)
h = socket.gethostname()

# get stock quote and populate list
for symbol in symbols:
    r = requests.get(stockurl + symbol)
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
