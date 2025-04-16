from flask import Blueprint, request, jsonify
from .logic import get_prediction
from .models import PredictionLog
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def hello_world():
    return "<p>Hello, Safe Pick!</p>"


@main.route("/predict", methods=["POST"])
def predict():
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    data = request.get_json()
    amount = data.get("amount")
    tenor = data.get("tenor")

    if not amount or not tenor:
        return jsonify({"error": "amount and tenor required"}), 400

    result = get_prediction(amount, tenor)
    result["profit_gold"] = round(float(result["profit_gold"]), 2)
    result["predicted_gold_price"] = round(float(result["predicted_gold_price"]), 2)

    # store prediction log to db for future analysis
    log = PredictionLog(
        amount=amount,
        tenor=tenor,
        predicted_price=result["predicted_gold_price"],
        profit_gold=result["profit_gold"],
        profit_deposit=result["profit_deposit"],
        recommendation=result["recommend"],
        ip_address=ip_address,
    )

    db.session.add(log)
    db.session.commit()

    return jsonify(result)


@main.route("/logs", methods=["GET"])
def get_logs():
    logs = PredictionLog.query.order_by(PredictionLog.timestamp.desc()).limit(100).all()
    return jsonify([log.to_dict() for log in logs])
