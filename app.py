from flask import Flask, request, jsonify
from flask_cors import CORS
from slvs_helper import Slvs_Helper

app = Flask(__name__)
CORS(app)

my_slvs_helper = Slvs_Helper()


@app.route('/solve', methods=['POST'])
def post_data():
    global my_slvs_helper
    if request.is_json:
        data = request.get_json()

        print("Data received:", data)

        for entity in data["entities"]:
            if entity["t"] == "point":
                my_slvs_helper.addPoint(data["workplane"], entity["id"], entity["v"])
            elif entity["t"] == "line":
                my_slvs_helper.addLine(data["workplane"], entity["id"], entity["v"])
            elif entity["t"] == "circle":
                my_slvs_helper.addCircle(data["workplane"], entity["id"], entity["v"])
            else:
                print("Warning entity of type %s not yet supported" % entity.t)
        for constraint in data["constraints"]:
            my_slvs_helper.addConstraint(data["workplane"], constraint["id"], constraint["t"], constraint["v"])

        code, a, b = my_slvs_helper.solve()

        result = {"code": code}
        print("code=%d" % code)
        if code == 0:
            print("dof=%d" % a)
            print("changed entities")
            print(b)
            result["dof"] = a
            result["entities"] = b
            result["failed"] = []
        else:
            print("failed:")
            print(a)
            result["failed"] = a
            result["dof"] = -1
            result["entities"] = []

        # Reset the state of the solver, to be changed
        my_slvs_helper = Slvs_Helper()

        return jsonify(result), 200
    else:
        # Request does not contain json
        return jsonify({"error": "Request does not contain JSON data"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=7777)
