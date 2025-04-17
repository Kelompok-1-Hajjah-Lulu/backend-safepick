from flask import Blueprint, request, jsonify
from .models import PredictionLog
from . import db
from .logic import get_prediction, get_prediction_all
from datetime import datetime, time
from sqlalchemy import and_

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

    # --- Caching logic: check if prediction already exists in db for today after 2 AM UTC (9 AM GMT+7) ---
    now = datetime.utcnow()
    today_2am_utc = datetime.combine(now.date(), time(2, 0))  # 2 AM UTC == 9 AM GMT+7

    cached_log = (
        PredictionLog.query.filter(
            and_(
                PredictionLog.amount == amount,
                PredictionLog.tenor == tenor,
                PredictionLog.timestamp >= today_2am_utc,
            )
        )
        .order_by(PredictionLog.timestamp.desc())
        .first()
    )

    if cached_log:
        return jsonify(cached_log.to_predict_result_dict())

    # --- no cache: use machine learning model to predict ---
    result = get_prediction(amount, tenor)
    result["profit_gold"] = round(float(result["profit_gold"]), 2)
    result["predicted_gold_price"] = round(float(result["predicted_gold_price"]), 2)

    # store prediction log to db for future analysis
    log = PredictionLog(
        amount=amount,
        tenor=tenor,
        predicted_price=result["predicted_gold_price"],
        predicted_buyback=result["predicted_buyback"],
        gold_gram=result["gold_gram"],
        profit_gold=result["profit_gold"],
        profit_deposit=result["profit_deposit"],
        gold_return_rate=result["gold_return_rate"],
        deposit_return_rate=result["deposit_return_rate"],
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


@main.route("/predicts-all", methods=["POST"])
def predict_all():
    data = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"error": "amount and tenor required"}), 400

    result = get_prediction_all(amount)

    return jsonify(result)
