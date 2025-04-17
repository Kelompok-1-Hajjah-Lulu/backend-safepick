from . import db
from datetime import datetime


class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    tenor = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    predicted_buyback = db.Column(db.Float, nullable=True)
    gold_gram = db.Column(db.Float, nullable=True)
    profit_gold = db.Column(db.Float, nullable=False)
    profit_deposit = db.Column(db.Float, nullable=False)
    gold_return_rate = db.Column(db.Float, nullable=True)
    deposit_return_rate = db.Column(db.Float, nullable=True)
    recommendation = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "tenor": self.tenor,
            "ip_address": self.ip_address,
            "gold_return_rate": self.gold_return_rate,
            "deposit_return_rate": self.deposit_return_rate,
            "gold_gram": self.gold_gram,
            "predicted_buyback": self.predicted_buyback,
            "predicted_gold_price": self.predicted_price,
            "profit_gold": self.profit_gold,
            "profit_deposit": self.profit_deposit,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_predict_result_dict(self):
        return {
            "deposit_return_rate": self.deposit_return_rate,
            "gold_gram": self.gold_gram,
            "gold_return_rate": self.gold_return_rate,
            "predicted_buyback": self.predicted_buyback,
            "predicted_gold_price": self.predicted_price,
            "profit_deposit": self.profit_deposit,
            "profit_gold": self.profit_gold,
            "recommend": self.recommendation,
        }
