from azure.storage.queue import QueueService
import json
import os
import random
import requests

# grab environment variables
azurestoracct = os.environ['azurestoracct']
azurequeue = os.environ['azurequeue']
azurequeuekey = os.environ['azurequeuekey'] + "==;"
image = os.environ['image']

if "delay" in os.environ:
    delay = os.environ['delay']
else:
    delay = 0

if "docker" in os.environ:
    docker = os.environ['docker']

if "chronos" in os.environ:
    chronos = os.environ['chronos']

while True:
    # set up azure queue
    queue_service = QueueService(account_name=azurestoracct, account_key=azurequeuekey)

    # get messages from azure queue
    messages = queue_service.get_messages(azurequeue, num_messages=5)

    # delete from queue, create container, start container
    for message in messages:
        
        # delete message from azure queue
        queue_service.delete_message(azurequeue, message.id, message.pop_receipt)
                
        if "docker" in os.environ:

            # sample json
            # {"Image": "neilpeterson/stock-report","Cmd": ["--symbols=msft;lnkd", "--email=nepeters@microsoft.com"],"Env": ["gmuser = xneilpetersonx@gmail.com", "gmpass = TempForDemo2016"]}
            s = message.content.split(':')
            data = json.loads('{"Image": "' + image + '","Cmd": ["--symbols=' + s[0] +'", "--email=' + s[1] + '","--delay=' + str(delay) + '"]}')
            print(data)
        
            # create and start docker container
            headers = {'Content-Type': 'application/json'}
            r = requests.post(docker + "create", data=json.dumps(data), headers=headers)
            b = json.loads(r.text)
            x = requests.post(docker + b['Id'] + "/start")

        if "chronos" in os.environ:

            randomint = random.randint(1, 100000)
            
            # sample json
            # {"schedule": "R0/2016-09-28T22:55:00Z/PT24H", "name": "docker08", "cpus": "0.1", "mem": "32", "command": "docker run -e reportdelay=120 -e gmuser=xneilpetersonx@gmail.com -e gmpass=TempForDemo2016 neilpeterson/stock-report-linux --symbols=msft --email=neil.peterson@microsoft.com"}
            s = message.content.split(':')
            data = json.loads('{"schedule": "R0/2016-09-28T22:55:00Z/PT24H","name":"' + str(randomint) + '","cpus": "0.1","mem": "32","command": "docker run ' + image + ' --symbols=' + s[0] + ' --email=' + s[1] + ' --delay=' + str(delay) + '"}')
            print(data)

            # create and start docker container
            headers = {'Content-Type': 'application/json'}
            r = requests.post(chronos + "scheduler/iso8601", data=json.dumps(data), headers=headers)
            x = requests.put(chronos + 'scheduler/job/' + str(randomint))