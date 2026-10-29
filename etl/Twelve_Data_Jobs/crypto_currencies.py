import json
from sqlalchemy import text
from etl.database import get_engine
import logging
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()



url =  "https://api.twelvedata.com/cryptocurrencies"

logger = logging.getLogger(__name__)


def load_crypto_currencies():
    logger.info("Crypto Currencies ETL started")

    
    try:
        api_key = os.getenv("TWELVE_DATA_KEY")

        if not api_key:
             raise ValueError("API key can not be found!")
   
        engine = get_engine()
        
        
        response = requests.get(
        url=url,
        headers={"Authorization":f"apikey {api_key}"},
        timeout=30
    )

        response.raise_for_status()

        result = response.json()

        if result.get("status") == "error":
            raise RuntimeError(result.get("message","API hatası"))

        json.dumps(result,indent=4, ensure_ascii=False)

        df = pd.DataFrame(result["data"])
        
        if df.empty:
            raise ValueError("API returned empty dataset")
        
        expected_columns = [
            "symbol",
            "available_exchanges",
            "currency_base",
            "currency_quote"
        ]
        
        df = df[expected_columns].copy()
        
        df["available_exchanges"] = df["available_exchanges"].apply(json.dumps)
        
        with engine.begin() as conn:
            df.to_sql(
                name="tmp_crypto_currencies",
                con=conn,
                schema="src",
                if_exists="replace",
                index=False
            )
            
            conn.execute(text
                         ("""Truncate Table src.crypto_currencies 
                          RESTART IDENTITY"""
                          )
                         )

            conn.execute(text(""" INSERT INTO src.crypto_currencies(
                symbol,available_exchanges,currency_base,currency_quote )
                
                select 
                    symbol,
                    available_exchanges::jsonb,
                    currency_base,
                    currency_quote
                FROM src.tmp_crypto_currencies
                """))
            
            conn.execute(text(""" drop table src.tmp_crypto_currencies"""))
            
            logger.info(
            "Crypto Currencies ETL completed. Rows: %s",
            len(df))

    except Exception:
        logger.exception("Crypto Currencies etl failed")
        raise
