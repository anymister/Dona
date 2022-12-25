# Importez les bibliothèques nécessaires
import openai
import requests
import json

# Remplacez YOUR_API_KEY par votre clé d'API et PAGE_ACCESS_TOKEN par votre jeton d'accès de page
openai.api_key = "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"
PAGE_ACCESS_TOKEN = "EAARFNY9Vz1UBAH2465vUKpAw5QUDnGsBNZBE4DnPlmTY3pLLI6lkOWL9UvcY3d6BF26nIXPFmOfF84xPygHtl1XHmmEf8fIQcVMkUkEEPiCiWObgzVPfLJPzPQAqlEvVphqZBejrsRGVRUACP2Fy7VZClWYLv53jb436P34z5tTpkcr5MU5"

def ask_question(prompt):
  # Envoyez une demande à l'API de ChatGPT en utilisant la méthode completions
  response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      
      n=1,
      stop=None,
      stream=None,
      
      temperature=0.5,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )

  # Affichez la réponse du modèle
  return response["choices"][0]["text"]

def send_message(recipient_id, message):
  # Envoyez un message à l'utilisateur via l'API de Messenger
  params = {
      "access_token": PAGE_ACCESS_TOKEN
  }
  headers = {
      "Content-Type": "application/json"
  }
  data = json.dumps({
      "recipient": {
          "id": recipient_id
      },
      "message": {
          "text": message
      }
  })
  r = requests.post("https://graph.facebook.com/v6.0/me/messages", params=params, headers=headers, data=data)

def handle_message(event):
  # Traitez les messages reçus via l'API de Messenger
  sender_id = event["sender"]["id"]
  message = event["message"]["text"]

  # Demandez une réponse au chatbot
  response = ask_question(message)

  # Envoyez la réponse à l'utilisateur
  send_message(sender_id, response)

def handle_webhook(request):
  # Traitez les demandes de webhook envoyées par l'API de Messenger
  if request.method == "POST":
    event = request.json
    handle_message(event)
    return "ok", 200
  else:
    return "ok", 200
