from flask import Flask, request, jsonify
from flask_cors import CORS
from slvs_helper import Slvs_Helper

app = Flask(__name__)
CORS(app)

my_slvs_helper = Slvs_Helper()

"""
export interface SolverRequestType {
    workplane: string;
    entities: {id: number, t: "point" | "line" | "circle" | "arc", v: number[]}[];
    constraints: {id: number, t: SlvsConstraints, v: number[]}[];
}

export interface SolverResponseType {
    code: number;
    failed: number[];
    entities: {id: number, t: "point" | "line" | "circle" | "arc", v: number[]}[];
    dof: number;
}
"""

# POST-Endpunkt
@app.route('/solve', methods=['POST'])
def post_data():
    global my_slvs_helper
    # Überprüfen, ob die Anfrage JSON-Daten enthält
    if request.is_json:
        # JSON-Daten aus der Anfrage erhalten
        data = request.get_json()

        # Hier kannst du mit den empfangenen Daten arbeiten
        # Zum Beispiel könntest du sie in die Konsole drucken
        print("Empfangene Daten:", data)

        for entity in data["entities"]:
            if entity["t"] == "point":
                my_slvs_helper.addPoint(data["workplane"], entity["id"], entity["v"])
            elif entity["t"] == "line":
                my_slvs_helper.addLine(data["workplane"], entity["id"], entity["v"])
            else:
                print("Warning entity of type %s not yet supported" % entity.t)
        for constraint in data["constraints"]:
            my_slvs_helper.addConstraint(data["workplane"], constraint["id"], constraint["t"], constraint["v"])

        result, a, b = my_slvs_helper.solve()

        # TODO generate the proper result
        print("result=%d" % result)
        if result == 0:
            print("dof=%d" % a)
            print("changed entities")
            print(b)
        else:
            print("failed:")
            print(a)

        # hack to reset the state of the solver, to be changed
        my_slvs_helper = Slvs_Helper()

        # Beispielantwort zurückgeben
        return jsonify({"message": "Daten empfangen"}), 200
    else:
        # Falls keine JSON-Daten in der Anfrage enthalten sind
        return jsonify({"error": "Anfrage enthält keine JSON-Daten"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=7777)
