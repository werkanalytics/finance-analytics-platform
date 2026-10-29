import pandas as pd
import yfinance as yf
from sqlalchemy import text
from etl.database import get_engine
import logging

logger = logging.getLogger(__name__)


def validate_balance_sheet(row:dict) -> bool:
    if not row["ticker"]:
        raise ValueError("Ticker cannot be empty")
    
    if not row["metric_name"]:
        raise ValueError("Metric name cannot be empty")
    
    if pd.isna(row["report_date"]):
        raise ValueError("Report date cannot be empty")
    
    if pd.isna(row["metric_value"]):
        raise ValueError("Metric value cannot be empty")

    return True
                    
    
            
            


def load_balance_sheet():
    logger.info("Balance sheet ETL started")
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
                fin = yf.Ticker(symbol).balance_sheet

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

                logger.info("%s balance sheet completed", symbol)

            except Exception:
                logger.exception("%s balance sheet failed", symbol)
                
                

        if not financial_rows:
            logger.warning("No balance sheet data found")
            return
            

        financial_df = pd.concat(financial_rows, ignore_index=True)

        with engine.begin() as conn:
            for _, row in financial_df.iterrows():
                validate_balance_sheet(row.to_dict())
                
                
                conn.execute(
                    text("""
                        INSERT INTO src.balance_sheet (
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
        logger.exception("Balance sheet ETL failed")
        raise
    
    logger.info("Balance sheet loaded successfully")
        
    