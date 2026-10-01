import pandas as pd
import yfinance as yf
from sqlalchemy import text
from etl.database import get_engine
import logging

logger = logging.getLogger(__name__)


def load_financials():
    logger.info("Financials ETL started")
    try:
        
        engine = get_engine()
        

        tickers_src = pd.read_sql(
            "SELECT ticker FROM src.tickers",
            engine
        )

        tickers = tickers_src["ticker"].tolist()
        financial_rows = []

        for symbol in tickers:
            try:
                fin = yf.Ticker(symbol).financials

                if fin.empty:
                    continue

                fin = fin.reset_index()
                fin.rename(columns={"index": "metric_name"}, inplace=True)

                fin = fin.melt(
                    id_vars=["metric_name"],
                    var_name="report_date",
                    value_name="metric_value"
                )

                fin["ticker"] = symbol
                fin["report_date"] = pd.to_datetime(fin["report_date"]).dt.date

                financial_rows.append(fin)

                print(f"{symbol} financials tamamlandı")

            except Exception:
                raise ValueError("Failed to fetch financials data for %s", symbol)

        if not financial_rows:
            logger.exception("No financial rows data found")
        

        financial_df = pd.concat(financial_rows, ignore_index=True)

        with engine.begin() as conn:
            for _, row in financial_df.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO src.financials (
                            ticker,
                            metric_name,
                            report_date,
                            metric_value
                        )
                        VALUES (
                            :ticker,
                            :metric_name,
                            :report_date,
                            :metric_value
                        )
                        ON CONFLICT (ticker, metric_name, report_date)
                        DO UPDATE SET
                            metric_value = EXCLUDED.metric_value
                    """),
                    row.to_dict()
                )
    except Exception:
        logger.exception("Financials etl failed")
        raise

    logger.info("Financials table loaded successfully.")