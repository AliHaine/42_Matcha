import socketio
from time import sleep

# Créer une instance de SimpleClient
client = socketio.Client()

# Définir un gestionnaire d'événements pour écouter les réponses du serveur
@client.on('response')
def handle_my_response(data):
    print('Received response from server:', data)

# Connexion au serveur
client.connect('http://localhost:5000')

# Émettre un événement vers le serveur
client.emit('my event', {'data': 'foobar'})

# Attendre pour recevoir des réponses
sleep(5)

while True:
    event = input("Enter event to send:")
    if event == "exit":
        break
    message = input("Enter message to send:")
    client.emit(event, '{"data": "' + message + '"}')

# Déconnexion du serveur
client.disconnect()