from azure.storage.queue import QueueService
import requests
import json

# variables – needs azure queue name, key, and docker api url 
storagacct = "<acct>"
queue = "<queue>"
queuekey = "<queue key>"
docker = "http://<docker host>:2375/containers/"
image = "neilpeterson/stock-report"

while True:
    # set up azure queue
    queue_service = QueueService(account_name=storagacct, account_key=queuekey)

    # get messages from azure queue
    messages = queue_service.get_messages(queue, num_messages=5)

    # delete from queue, create container, start container
    for message in messages:
        
        # get stock symbols / email address and construct json
        # sample json "Image": "neilpeterson/stock-report", "Cmd": ["--symbols=msft;lnkd","--email=nepeters@microsoft.com"]}
        s = message.content.split(':')
        data = json.loads('{"Image": "' + image + '", "Cmd": ["--symbols=' + s[0] + '","--email=' + s[1] + '"]}')
        print(data)

        # delete message from azure queue
        queue_service.delete_message(queue, message.id, message.pop_receipt)
        
        # create and start docker container
        headers = {'Content-Type': 'application/json'}
        r = requests.post(docker + "create", data=json.dumps(data), headers=headers)
        b = json.loads(r.text)
        x = requests.post(docker + b['Id'] + "/start")
