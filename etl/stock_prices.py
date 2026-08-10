import pandas as pd
import yfinance as yf
from sqlalchemy import text

from etl.database import get_engine


def load_stock_prices():
    engine = get_engine()

    tickers_df = pd.read_sql(
        "SELECT ticker FROM src.tickers",
        engine
    )

    tickers = tickers_df["ticker"].tolist()

    df = yf.download(
        tickers,
        period="5y",
        auto_adjust=True,
        group_by="ticker"
    )

    df = df.stack(level=0).reset_index()

    df = df.rename(columns={
        "Date": "price_date",
        "Ticker": "ticker",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume"
    })

    df = df[[
        "price_date",
        "ticker",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]]

    df["price_date"] = pd.to_datetime(df["price_date"]).dt.date

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO src.stock_prices (
                        price_date,
                        ticker,
                        open_price,
                        high_price,
                        low_price,
                        close_price,
                        volume
                    )
                    VALUES (
                        :price_date,
                        :ticker,
                        :open_price,
                        :high_price,
                        :low_price,
                        :close_price,
                        :volume
                    )
                    ON CONFLICT (ticker, price_date)
                    DO UPDATE SET
                        open_price = EXCLUDED.open_price,
                        high_price = EXCLUDED.high_price,
                        low_price = EXCLUDED.low_price,
                        close_price = EXCLUDED.close_price,
                        volume = EXCLUDED.volume
                """),
                row.to_dict()
            )

    print("Stock prices loaded successfully.")