@app.route("/webhook", methods=["GET"])
def verify_webhook():
  # Récupérez le jeton de vérification envoyé par Messenger
  verify_token = request.args.get("hub.verify_token")

  # Vérifiez que le jeton de vérification est correct
  if verify_token == "my_verify_token":
    # Renvoyez le jeton de vérification à Messenger
    return request.args.get("hub.challenge")
  else:
    # Renvoyez une réponse vide si le jeton de vérification est incorrect
    return "le jeton est incorrect"
