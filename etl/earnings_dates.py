import pandas as pd
import yfinance as yf
from etl.database import get_engine
from sqlalchemy import text




def load_earnings_dates():
    engine = get_engine()

    tickers = pd.read_sql(
        "SELECT ticker FROM src.tickers",
        engine
    )["ticker"].tolist()

    rows = []

    for symbol in tickers:
        try:
            df = yf.Ticker(symbol).earnings_dates

            if df.empty:
                continue

            df = df.reset_index()

            df = df.rename(columns={
                "Earnings Date": "earnings_date",
                "EPS Estimate": "eps_estimate",
                "Reported EPS": "reported_eps",
                "Surprise(%)": "surprise_pct"
            })

            df["ticker"] = symbol
            df["earnings_date"] = pd.to_datetime(df["earnings_date"])
            df["loaded_at"] = pd.Timestamp.utcnow()

            rows.append(df)

            print(f"{symbol} earnings dates tamamlandı")

        except Exception as e:
            print(f"{symbol} hata: {e}")

    if not rows:
        print("Earnings dates verisi bulunamadı.")
        return

    final_df = pd.concat(rows, ignore_index=True)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE src.earnings_dates"))

    final_df.to_sql(
        "earnings_dates",
        engine,
        schema="src",
        if_exists="append",
        index=False
    )

    print("Earnings dates tablosu yüklendi.")

if __name__ == "__main__":
    load_earnings_dates()