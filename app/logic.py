from .model_loader import load_model_and_pipeline, predict_future_prices
import pandas as pd

GRR = 9.050577 / 100
BUYBACK_DIFF = 149419.3548
DATA_PATH = "data/antam_price_2025_4_14.csv"


def get_nisbah(amount, tenure):
    # menggunakan rate di byond untuk <12 bulan
    if tenure < 12:
        if tenure <= 3 and amount < 100_000_000:
            return 0.28
        elif (tenure == 6 and amount < 100_000_000) or (amount < 1_000_000_000):
            return 0.29
        elif (tenure == 6 and amount < 1_000_000_000) or (
            amount == 1_000_000_000 and tenure <= 3
        ):
            return 0.3
        elif tenure == 6 and amount == 1_000_000_000:
            return 0.31
    # menggunakan rate di cabang untuk tenor 12 bulan
    elif tenure == 12:
        if amount < 1_000_000_000:
            return 0.26
        elif amount == 1_000_000_000:
            return 0.27


def get_prediction(amount, tenure):
    model, pipeline = load_model_and_pipeline()
    df = pd.read_csv(DATA_PATH, index_col=0)
    df.index = pd.to_datetime(df.index)
    df_weekly = df.resample("W").mean().ffill().iloc[-17:]

    # Predict gold price

    predicted_prices = predict_future_prices(df_weekly, model, pipeline, tenure)
    predicted_gold_price = predicted_prices[-1]
    predicted_buyback = predicted_gold_price - BUYBACK_DIFF

    latest_gold_price = df.iloc[-1, 0]
    gold_gram = amount / latest_gold_price
    gold_profit = (gold_gram * predicted_buyback) - amount

    nisbah = get_nisbah(amount, tenure)
    deposit_profit = (GRR * nisbah * amount / 12) * tenure

    gold_return_rate = (gold_profit / amount) * 100
    deposit_return_rate = (deposit_profit / amount) * 100

    recommendation = "gold" if gold_profit > deposit_profit else "deposit"

    return {
        "recommend": recommendation,
        "profit_gold": round(gold_profit, 2),
        "profit_deposit": round(deposit_profit, 2),
        "predicted_gold_price": round(predicted_gold_price, 2),
        "gold_gram": round(gold_gram, 4),
        "predicted_buyback": round(predicted_buyback, 2),
        "gold_return_rate": round(gold_return_rate, 2),
        "deposit_return_rate": round(deposit_return_rate, 2),
    }


def get_prediction_all(amount):
    model, pipeline = load_model_and_pipeline()
    df = pd.read_csv(DATA_PATH, index_col=0)
    df.index = pd.to_datetime(df.index)
    df_weekly = df.resample("W").mean().ffill().iloc[-17:]
    tenure_one_year = 12
    latest_gold_price = df.iloc[-1, 0]

    # Predict gold price
    predicted_prices = predict_future_prices(
        df_weekly, model, pipeline, tenure_one_year
    )
    gold_gram = amount / latest_gold_price
    results = {}

    results["gold_gram"] = round(gold_gram, 4)

    for tenure in [3, 12, 25, 51]:
        predicted_gold_price = predicted_prices[tenure]
        predicted_buyback = predicted_gold_price - BUYBACK_DIFF

        gold_profit = (gold_gram * predicted_buyback) - amount

        tenure_months = {3: 1, 12: 3, 25: 6, 51: 12}.get(tenure)
        nisbah = get_nisbah(amount, tenure_months)
        deposit_profit = (GRR * nisbah * amount / 12) * tenure_months

        gold_return_rate = (gold_profit / amount) * 100
        deposit_return_rate = (deposit_profit / amount) * 100

        result = {}
        result["profit_gold"] = round(gold_profit, 2)
        result["profit_deposit"] = round(deposit_profit, 2)
        result["predicted_gold_price"] = round(predicted_gold_price, 2)
        result["predicted_buyback"] = round(predicted_buyback, 2)
        result["tenure"] = tenure_months
        result["gold_return_rate"] = round(gold_return_rate, 2)
        result["deposit_return_rate"] = round(deposit_return_rate, 2)

        results[f"tenure_{tenure_months}"] = result

    return results
