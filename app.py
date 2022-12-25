from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
  if request.method == "POST":
    # Récupérez le message envoyé par l'utilisateur
    message = request.get_json()
    print(message)

    # Envoyez une réponse à l'utilisateur en utilisant l'API de chatgpt
    response = requests.post(
      "https://api.openai.com/v1/chatgpt",
      headers={"Content-Type": "application/json", "Authorization": "Bearer YOUR_API_KEY"},
      json={"prompt": message["text"], "model": "chatgpt"}
    )

    # Récupérez la réponse de l'API de chatgpt
    response_text = response.json()["response"]

    # Envoyez la réponse à l'utilisateur via l'API de Messenger
    requests.post(
      "https://graph.facebook.com/v6.0/me/messages",
      params={"access_token": "YOUR_MESSENGER_ACCESS_TOKEN"},
      json={
        "recipient": {"id": message["sender"]["id"]},
        "message": {"text": response_text}
      }
    )

  # Renvoyez une réponse vide pour indiquer que le webhook a été reçu
  return ""

if __name__ == "__main__":
  app.run()
