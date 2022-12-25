import openai
import os
import requests
import json

openai.api_key = os.environ["openia_token"]

def generate_response(prompt):
  completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
  )

  message = completions.choices[0].text
  return message

def handle_message(event):
  sender_id = event['sender']['id']
  message = event['message']['text']
  response = generate_response(prompt=message)

  send_message(sender_id, response)

def send_message(recipient_id, message):
  params = {
    "access_token": os.environ["page_token"]
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

def verify_webhook(req):
  if req.args.get("hub.mode") == "subscribe" and req.args.get("hub.challenge"):
    if not req.args.get("hub.verify_token") == os.environ["verify_token"]:
      return "Verification token mismatch", 403
    return req.args["hub.challenge"], 200

  return "Hello world", 200

def handle_webhook(req):
  if req.method == "POST":
    print("Handling POST request")
    data = json.loads(req.data)
    if data["object"] == "page":
      for entry in data["entry"]:
        for messaging_event in entry["messaging"]:
          if messaging_event.get("message"):
            handle_message(messaging_event)
          else:
            print("Unknown event: ", messaging_event)
    return "OK", 200
  else:
    print("Invalid request method")
    return "Invalid request method", 405
