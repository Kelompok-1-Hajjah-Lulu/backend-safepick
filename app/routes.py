from flask import Blueprint, request, jsonify
from .logic import get_prediction

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
    return jsonify(result)
