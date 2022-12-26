from flask import Flask, request
import os

app = Flask(__name__)

# Récupérez les variables d'environnement
API_KEY = os.environ["API_KEY"]
MESSENGER_ACCESS_TOKEN = os.environ["MESSENGER_ACCESS_TOKEN"]

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "GET":
    # Vérifiez que le jeton de vérification envoyé par Messenger est correct
    verify_token = request.args.get("hub.verify_token")
    if verify_token == "my_verify_token":
      # Renvoyez le jeton de vérification à Messenger
      return request.args.get("hub.challenge")
    else:
      # Renvoyez une réponse vide si le jeton de vérification est incorrect
      return ""
  elif request.method == "POST":
    # Récupérez le message envoyé par l'utilisateur
    message = request.get_json()
    print(message)

    # Envoyez une réponse à l'utilisateur en utilisant l'API de chatgpt
    response = requests.post(
      "https://api.openai.com/v1/chatgpt",
      headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
      json={"prompt": message["text"], "model": "chatgpt"}
    )

    # Récupérez la réponse de l'API de chatgpt
    response_text = response.json()["response"]

    # Envoyez la réponse à l'utilisateur via l'API de Messenger
    requests.post(
      "https://graph.facebook.com/v6.0/me/messages",
      params={"access_token": MESSENGER_ACCESS_TOKEN},
      json={
        "recipient": {"id": message["sender"]["id"]},
        "message": {"text": response_text}
      }
    )

  # Renvoyez une réponse vide pour indiquer que le webhook a été reçu
  return ""
