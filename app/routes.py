from flask import Blueprint, request, jsonify
from .logic import get_prediction,get_prediction_all

main = Blueprint("main", __name__)

@main.route("/")
def hello_world():
    return "<p>Hello, Safe Pick!</p>"

@main.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    amount = data.get("amount")
    tenor = data.get("tenor")

    if not amount or not tenor:
        return jsonify({"error": "amount and tenor required"}), 400

    result = get_prediction(amount, tenor)
    result["profit_gold"] = round(float(result["profit_gold"]), 2)
    result["predicted_gold_price"] = round(float(result["predicted_gold_price"]), 2)
    result["gold_gram"] = round(float(result["gold_gram"]), 4)
    return jsonify(result)

@main.route("/predicts-all", methods=["POST"])
def predict_all():
    data = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "amount and tenor required"}), 400
    
    result = get_prediction_all(amount)
    
    return jsonify(result)

