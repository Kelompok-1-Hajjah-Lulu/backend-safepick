import pickle
from tensorflow.keras.models import model_from_json
import numpy as np
import pandas as pd


def load_model_and_pipeline():
    with open("models/pipeline_v2.pkl", "rb") as f:
        pipeline = pickle.load(f)
    with open("models/gold_1week_architecture_v2.pkl", "rb") as f:
        model_json = pickle.load(f)
    with open("models/gold_1week_weights_v2.pkl", "rb") as f:
        weights = pickle.load(f)
    model = model_from_json(model_json)
    model.set_weights(weights)
    return model, pipeline


def prepare_input(df, pipeline, input_window=13, diff_lag=4):
    prices_series = df.iloc[:, 0]
    diff = prices_series - prices_series.shift(diff_lag)
    df_features = pd.DataFrame({"price": prices_series, "diff_4w": diff.dropna()})
    recent = df_features.iloc[-input_window:]
    X_input = recent.to_numpy().reshape(1, input_window, 2)
    X_scaled = pipeline.transform(X_input.reshape(-1, 1)).reshape(X_input.shape)
    return X_scaled


def predict_future_prices(df_weekly, model, pipeline, tenure):
    df_temp = df_weekly.copy()
    weeks = {1: 4, 3: 13, 6: 26, 12: 52}.get(tenure)
    if weeks is None:
        raise ValueError("Invalid tenure")

    scaler = pipeline.named_steps["preprocessor"].named_transformers_["scale"]
    results = []

    for _ in range(weeks):
        X = prepare_input(df_temp, pipeline)
        pred_scaled = model.predict(X, verbose=0)
        pred_price = scaler.inverse_transform(pred_scaled)[0][0]
        results.append(float(pred_price))

        last_date = df_temp.index[-1]
        next_row = pd.DataFrame(
            [[pred_price]],
            index=[last_date + pd.Timedelta(weeks=1)],
            columns=df_temp.columns,
        )
        df_temp = pd.concat([df_temp, next_row])

    return results
