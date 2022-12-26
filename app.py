import os
import openai
from flask import Flask, request

app = Flask(__name__)

# Récupérez les variables d'environnement
API_KEY = os.environ["API_KEY"]
MESSENGER_ACCESS_TOKEN = os.environ["MESSENGER_ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

# Configurez l'API OpenAI
openai.api_key = API_KEY

# Définissez la fonction qui utilise chatgpt pour répondre à l'utilisateur
def get_response(message):
  # Utilisez chatgpt pour générer une réponse
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"{message}\n",
    max_tokens=1024,
    temperature=0.7,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=1
  )
  return response.text.strip()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "GET":
    # Vérifiez que le jeton de vérification envoyé par Messenger est correct
    if verify_token == request.args.get("hub.verify_token"):
      # Renvoyez le jeton de vérification à Messenger
      return request.args.get("hub.challenge")
    else:
      # Renvoyez une réponse vide si le jeton de vérification est incorrect
      return ""
  elif request.method == "POST":
    # Récupérez le message envoyé par l'utilisateur
    data = request.get_json()
    print(data)

    # Récupérez l'ID de l'utilisateur et le message envoyé
    user_id = data["entry"][0]["messaging"][0]["sender"]["id"]
    message = data["entry"][0]["messaging"][0]["message"]["text"]

    # Utilisez chatgpt pour générer une réponse
    response = get_response(message)

    # Envoyez la réponse à l'utilisateur via l'API de Messenger
    send_message(user_id, response)

    # Renvoyez une réponse vide
    return ""

# Définissez la fonction qui envoie un message à l'utilisateur via l'API de Messenger
def send_message(recipient_id, message):
  # Envoyez le message à l'utilisateur
  params = {
    "access_token": MESSENGER_ACCESS_TOKEN
  }
  headers = {
    "Content-Type": "application/json"
  }
  data = {
    "recipient": {
      "id": recipient_id
    },
    "message": {
      "text": message
    }
  }
  r = requests.post("https://graph.facebook.com/v6.0/me/messages", params=params, headers=headers, data=json.dumps(data))
  if r.status_code != 200:
    print(r.status_code)
    print(r.text)

if __name__ == "__main__":
  app.run()
