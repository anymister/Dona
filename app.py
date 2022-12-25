import openai
import os
import requests

openai.api_key = os.environ["OPENAI_API_KEY"]

def handle_message(event, context):
  # Récupération du message envoyé par l'utilisateur
  message = event["message"]["text"]
  
  # Utilisation de ChatGPT pour générer une réponse
  response = openai.Completion.create(
    engine="chatgpt",
    prompt=message,
    max_tokens=1024
  ).text
  
  # Envoi de la réponse à l'utilisateur
  send_message(response)

def send_message(text):
  # Configuration de l'URL de l'API de Messenger
  api_url = "https://graph.facebook.com/v6.0/me/messages"
  params = {
    "access_token": os.environ["MESSENGER_ACCESS_TOKEN"]
  }
  
  # Construction du payload de la requête
  data = {
    "recipient": {
      "id": os.environ["MESSENGER_USER_ID"]
    },
    "message": {
      "text": text
    }
  }
  
  # Envoi de la requête à l'API de Messenger
  response = requests.post(api_url, params=params, json=data)

if response.status_code != 200:
  print("An error occurred:", response.text)
else:
  print("Successfully sent message:", text)
