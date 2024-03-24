from flask import Flask, request, jsonify
from slvs_helper import Slvs_Helper

app = Flask(__name__)

slvs_helper = Slvs_Helper()

# POST-Endpunkt
@app.route('/postdata', methods=['POST'])
def post_data():
    # Überprüfen, ob die Anfrage JSON-Daten enthält
    if request.is_json:
        # JSON-Daten aus der Anfrage erhalten
        data = request.get_json()

        # Hier kannst du mit den empfangenen Daten arbeiten
        # Zum Beispiel könntest du sie in die Konsole drucken
        print("Empfangene Daten:", data)

        # Beispielantwort zurückgeben
        return jsonify({"message": "Daten empfangen"}), 200
    else:
        # Falls keine JSON-Daten in der Anfrage enthalten sind
        return jsonify({"error": "Anfrage enthält keine JSON-Daten"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=7777)
