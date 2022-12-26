import requests

# Modifiez l'URL ci-dessous pour correspondre à l'URL de votre webhook
url = "https://your-chatbot-url.vercel.app/webhook"

# Modifiez le jeton de vérification ci-dessous pour correspondre au jeton de vérification de votre application sur Messenger
verify_token = "your-verify-token"

# Envoyez une requête GET à votre webhook en incluant le jeton de vérification
response = requests.get(url, params={"hub.verify_token": verify_token})

# Affichez la réponse de votre chatbot
print(response.text)
