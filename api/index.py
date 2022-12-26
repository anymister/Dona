import os
from flask import Flask, request

app = Flask(__name__)

# Récupérez les variables d'environnement
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

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
    message = request.get_json()
    print(message)

    # Renvoyez une réponse vide
    return ""

if __name__ == "__main__":
  app.run()
