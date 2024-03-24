import requests
import json

# URL des POST-Endpunkts der Flask-App
url = 'http://localhost:7777/postdata'

# JSON-Daten, die an den Endpunkt gesendet werden sollen
data = {
    'name': 'John Doe',
    'age': 30,
    'city': 'New York'
}

# Header für die Anfrage (optional)
headers = {'Content-Type': 'application/json'}

# Anfrage senden
response = requests.post(url, headers=headers, data=json.dumps(data))

# Antwort der Server-Anwendung ausgeben
print("Antwort vom Server:", response.text)
