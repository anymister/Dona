import os
import facebook
from flask import Flask, request

app = Flask(__name__)

# Récupérez votre jeton d'accès à partir de votre application Messenger sur le site de développeurs de Facebook
ACCESS_TOKEN = os.environ["MESSENGER_ACCESS_TOKEN"]

# Créez une instance de l'API de Messenger de Facebook en utilisant votre jeton d'accès
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="2.1")

def send_hello_message(sender_id):
    message = "Bonjour!"
    graph.send_message(
        message=message,
        recipient_id=sender_id,
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    # Récupérez l'ID de l'expéditeur du message à partir de la requête POST
    sender_id = request.json['entry'][0]['messaging'][0]['sender']['id']
    send_hello_message(sender_id)
    return "Success"

if __name__ == '__main__':
    app.run()
