from . import db
from datetime import datetime


class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    tenor = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    profit_gold = db.Column(db.Float, nullable=False)
    profit_deposit = db.Column(db.Float, nullable=False)
    recommendation = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "tenor": self.tenor,
            "ip_address": self.ip_address,
            "predicted_gold_price": self.predicted_price,
            "profit_gold": self.profit_gold,
            "profit_deposit": self.profit_deposit,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat(),
        }
