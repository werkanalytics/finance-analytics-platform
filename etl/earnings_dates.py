import pandas as pd
import yfinance as yf
from etl.database import get_engine
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)




def load_earnings_dates():
    logger.info("Earning dates etl has started")
    
    try:
        
    
        engine = get_engine()

        tickers = pd.read_sql("SELECT ticker FROM src.tickers",engine)["ticker"].tolist()

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

            except Exception:
                raise ValueError("Failed to fetch earning dates data for %s", symbol)

        if not rows:
            logger.exception("No earning dates data found.")
            
            
            

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
    except Exception:
        logger.exception("Earning dates ETL failed")
        raise

    logger.info("Earning dates loaded successfully")

if __name__ == "__main__":
    load_earnings_dates()