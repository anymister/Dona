from flask import Flask, request
import requests

app = Flask(__name__)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
  # Récupérez le jeton de vérification envoyé par Messenger
  verify_token = request.args.get("hub.verify_token")

  # Vérifiez que le jeton de vérification est correct
  if verify_token == os.environ["my_verify_token"]:
    # Renvoyez le jeton de vérification à Messenger
    return request.args.get("hub.challenge")
  else:
    # Renvoyez une réponse vide si le jeton de vérification est incorrect
    return ""
  
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "POST":
    # Récupérez le message envoyé par l'utilisateur
    message = request.get_json()
    print(message)

    # Envoyez une réponse à l'utilisateur en utilisant l'API de chatgpt
    response = requests.post(
      "https://api.openai.com/v1/chatgpt",
      headers={"Content-Type": "application/json", "Authorization": "Bearer " os.environ["YOUR_API_KEY"]},
      json={"prompt": message["text"], "model": "chatgpt"}
    )

    # Récupérez la réponse de l'API de chatgpt
    response_text = response.json()["response"]

    # Envoyez la réponse à l'utilisateur via l'API de Messenger
    requests.post(
      "https://graph.facebook.com/v6.0/me/messages",
      params={"access_token": os.environ["YOUR_MESSENGER_ACCESS_TOKEN"]},
      json={
        "recipient": {"id": message["sender"]["id"]},
        "message": {"text": response_text}
      }
    )

  # Renvoyez une réponse vide pour indiquer que le webhook a été reçu
  return ""

if __name__ == "__main__":
  app.run()
