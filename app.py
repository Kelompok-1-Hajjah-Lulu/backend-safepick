from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, Safe Pick!</p>"


# dummy for the prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    amount = data.get("amount")
    tenor = data.get("tenor")

    # TEMP logic, replace with model prediction later
    recommendation = "gold" if amount >= 2000000 and tenor >= 1 else "deposit"

    return jsonify({"amount": amount, "tenor": tenor, "recommend": recommendation})
