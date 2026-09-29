import pandas as pd
import yfinance as yf
from sqlalchemy import text
from etl.database import get_engine
import logging

logger = logging.getLogger(__name__)


def load_stock_prices():
    logger.info("Stock price ETL started")
    try:
        
        engine = get_engine()

        tickers_df = pd.read_sql(
            "SELECT ticker FROM src.tickers",
            engine
        )

        tickers = tickers_df["ticker"].tolist()
        
        if not tickers:
            raise ValueError("No tickers found in src.tickers")

        logger.info("Downloading prices for %s tickers", len(tickers))
                 

        df = yf.download(
            tickers,
            period="5y",
            auto_adjust=True,
            group_by="ticker"
        )
        
        if df.empty:
            raise ValueError("No stock price data returned from yfinance")
        
      

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
    except Exception:
        logger.exception("Stock price ETL failed")
        raise

    
    logger.info("Stock prices loaded successfully. Row count: %s",len(df))
    
    