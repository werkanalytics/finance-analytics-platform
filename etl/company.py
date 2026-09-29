import pandas as pd
import yfinance as yf
from sqlalchemy import text
from etl.database import get_engine
import logging

logger = logging.getLogger(__name__)



def load_company():
    logger.info("copmany ETL started")
    
    try:
        
        engine = get_engine()

        tickers_df = pd.read_sql(
            "SELECT ticker FROM src.tickers",
            engine
        )

        tickers = tickers_df["ticker"].tolist()
        
        if not tickers:
            raise ValueError("No tickers found in src.tickers")
        
        
        company_rows = []

        for symbol in tickers:
            try:
                info = yf.Ticker(symbol).info

                company_rows.append({
                    "ticker": symbol,
                    "company_name": info.get("longName"),
                    "sector": info.get("sector"),
                    "industry": info.get("industry"),
                    "country": info.get("country"),
                    "city": info.get("city"),
                    "exchange": info.get("exchange"),
                    "currency": info.get("currency"),
                    "website": info.get("website"),
                    "employee_count": info.get("fullTimeEmployees")
                })

                

            except Exception:
                logger.exception("Failed to fetch company data for %s", symbol)
                
        if not company_rows:
            raise ValueError("No company data returned from yfinance")

        company_df = pd.DataFrame(company_rows)
        
        logger.info("Company loaded successfully. Row count: %s",len(company_df))
        
        

        with engine.begin() as conn:
            for _, row in company_df.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO src.company (
                            ticker,
                            company_name,
                            sector,
                            industry,
                            country,
                            city,
                            exchange,
                            currency,
                            website,
                            employee_count
                        )
                        VALUES (
                            :ticker,
                            :company_name,
                            :sector,
                            :industry,
                            :country,
                            :city,
                            :exchange,
                            :currency,
                            :website,
                            :employee_count
                        )
                        ON CONFLICT (ticker) DO UPDATE SET
                            company_name = EXCLUDED.company_name,
                            sector = EXCLUDED.sector,
                            industry = EXCLUDED.industry,
                            country = EXCLUDED.country,
                            city = EXCLUDED.city,
                            exchange = EXCLUDED.exchange,
                            currency = EXCLUDED.currency,
                            website = EXCLUDED.website,
                            employee_count = EXCLUDED.employee_count
                    """),
                    row.to_dict()
                )
    except Exception:
        logger.exception("Comapny ETL failed")
        raise

    
    logger.info("Company loaded successfully")