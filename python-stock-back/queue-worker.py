from azure.storage.queue import QueueService
import os
import requests
import json

# grab environment variables
azurestoracct = os.environ['azurestoracct']
azurequeue = os.environ['azurequeue']
azurequeuekey = os.environ['azurequeuekey'] + "==;"
docker = os.environ['docker']
image = os.environ['image']

while True:
    # set up azure queue
    queue_service = QueueService(account_name=azurestoracct, account_key=azurequeuekey)

    # get messages from azure queue
    messages = queue_service.get_messages(azurequeue, num_messages=5)

    # delete from queue, create container, start container
    for message in messages:
        
        # get stock symbols / email address and construct json
        # sample json "Image": "neilpeterson/stock-report", "Cmd": ["--symbols=msft;lnkd","--email=nepeters@microsoft.com"]}
        s = message.content.split(':')
        data = json.loads('{"Image": "' + image + '", "Cmd": ["--symbols=' + s[0] + '","--email=' + s[1] + '"]}')
        print(data)

        # delete message from azure queue
        queue_service.delete_message(azurequeue, message.id, message.pop_receipt)
        
        # create and start docker container
        headers = {'Content-Type': 'application/json'}
        r = requests.post(docker + "create", data=json.dumps(data), headers=headers)
        b = json.loads(r.text)
        x = requests.post(docker + b['Id'] + "/start")
