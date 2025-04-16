from .model_loader import load_model_and_pipeline, predict_future_prices
import pandas as pd

GRR = 8.991301 / 100  # taruh di database
BUYBACK_DIFF = 149419.3548
DATA_PATH = "data/antam_price_2025_4_14.csv"

def get_nisbah(amount, tenure):
    if amount < 1000000000:
        return 0.25 if tenure <= 3 else 0.26
    elif amount < 5000000000:
        return 0.26 if tenure <= 3 else 0.27
    else:
        return 0.29

def get_prediction(amount, tenure):
    model, pipeline = load_model_and_pipeline()
    df = pd.read_csv(DATA_PATH, index_col=0)
    df.index = pd.to_datetime(df.index)
    df_weekly = df.resample("W").mean().ffill().iloc[-17:]

    # Predict gold price
    
    predicted_prices = predict_future_prices(df_weekly, model, pipeline, tenure)
    predicted_gold_price = predicted_prices[-1]
    predicted_buyback = predicted_gold_price - BUYBACK_DIFF

    gold_gram = amount / 1896000
    gold_profit = (gold_gram * predicted_buyback) - amount

    nisbah = get_nisbah(amount, tenure)
    deposit_profit = (GRR * nisbah * amount / 12) * tenure
    
    gold_return_rate = (gold_profit/amount)*100
    deposit_return_rate = (deposit_profit/amount)*100

    recommendation = "gold" if gold_profit > deposit_profit else "deposit"

    return {
        "recommend": recommendation,
        "profit_gold": round(gold_profit, 2),
        "profit_deposit": round(deposit_profit, 2),
        "predicted_gold_price": round(predicted_gold_price, 2),
        "gold_gram": round(gold_gram,4),
        "predicted_buyback": round(predicted_buyback, 2),
        "gold_return_rate": round(gold_return_rate,2), 
        "deposit_return_rate ": round(deposit_return_rate,2) 
    }
    
def get_prediction_all(amount):
    model, pipeline = load_model_and_pipeline()
    df = pd.read_csv(DATA_PATH, index_col=0)
    df.index = pd.to_datetime(df.index)
    df_weekly = df.resample("W").mean().ffill().iloc[-17:]
    tenure = 12

    # Predict gold price
    predicted_prices = predict_future_prices(df_weekly, model, pipeline, tenure)
    gold_gram = amount / 1896000
    results = {}
    
    results["gold_gram"]= round(gold_gram , 4)
    
    for tenor in [3,12,25,51]:
        predicted_gold_price = predicted_prices[tenor]
        predicted_buyback = predicted_gold_price - BUYBACK_DIFF

        gold_profit = (gold_gram * predicted_buyback) - amount

        nisbah = get_nisbah(amount, tenure)
        deposit_profit = (GRR * nisbah * amount / 12) * tenure
        
        tenure_months = {3: 1, 12: 3, 25: 6, 51: 12}.get(tenor)
        
        gold_return_rate = (gold_profit/amount)*100
        deposit_return_rate = (deposit_profit/amount)*100
        
        result = {}
        result["profit_gold"]= round(gold_profit, 2)
        result["profit_deposit"]= round(deposit_profit, 2)
        result["predicted_gold_price"]=round(predicted_gold_price, 2)
        result["predicted_buyback"]= round(predicted_buyback, 2)
        result["tenure"] = tenure_months
        result["gold_return_rate "] = round(gold_return_rate,2)
        result["deposit_return_rate "] = round(deposit_return_rate,2) 
        
        results[f"tenure_{tenure_months}"]= result

    return results
