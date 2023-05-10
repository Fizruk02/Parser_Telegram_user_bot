########IMPORT CONFIG############
import sys
sys.path.append('/var/www/html')
from include.parser import *
#################################

clients = {}
for bot_id in active_bots:
    clients[bot_id] = Client("../include/sessions/parser/"+str(bot_id))

def event_mess(client, message):
    if(not message.from_user.is_self):
        for client_key in clients:
            if(clients[client_key] == client and client_key != 16129789):
                data = requests.post(URL_TO_WEBHOOK, json={'user_api_key': client_key, 'data': json.dumps(str(message), ensure_ascii=True)})

for client in clients:
    clients[client].add_handler(MessageHandler(event_mess))
    clients[client].start()

idle()

for client in clients:
    clients[client].stop()