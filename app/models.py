from . import db
from datetime import datetime


class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    tenor = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    predicted_buyback = db.Column(db.Float, nullable=False)
    gold_gram = db.Column(db.Float, nullable=False)
    profit_gold = db.Column(db.Float, nullable=False)
    profit_deposit = db.Column(db.Float, nullable=False)
    gold_return_rate = db.Column(db.Float, nullable=False)
    deposit_return_rate = db.Column(db.Float, nullable=False)
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


class PredictionAllCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    result_json = db.Column(db.JSON, nullable=False)


class GoldPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    
class ApplicationForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    nomor_hp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kecamatan = db.Column(db.String(50), nullable=False)
    kota = db.Column(db.String(50), nullable=False)
    provinsi = db.Column(db.String(50), nullable=False)
    tipe_produk = db.Column(db.String(50), nullable=False)
    nominal = db.Column(db.Float, nullable=False)
    jangka_waktu = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    