import json
from sqlalchemy import text
from etl.database import get_engine
import logging
import os
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

url = "https://api.twelvedata.com/cryptocurrency_exchanges"

logger = logging.getLogger(__name__)


def load_crypto_currency_exchanges():
    logger.info("Crypto Currencies Exchanges ETL started")
    
    try:
        api_key = os.getenv("TWELVE_DATA_KEY")
        
        if not api_key:
            raise ValueError("API Key cannot be found")
        
        engine = get_engine()
        
        response = requests.get(
            url=url,
            headers={"Authorization":f"apikey {api_key}"},
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json
        
        if result.get("status") == "error":
            raise RuntimeError(result.get("message","API hatası"))
        
        json.dumps(result,indent=4, ensure_ascii=False)
        
        df = pd.DataFrame(result["data"])
        
        if df.empty:
            raise ValueError("API returned empty dataset")
        
        expected_columns = ["name"]
        
        df = df[expected_columns].copy()
        
        with engine.begin as conn:
            df.to_sql(
                name="tmp_crypto_exchanges",
                schema="src",
                if_exists="replace",
                index=False
            )
            
            
            conn.execute(text(""" TRUNCATE TABLE src.crypto_exchanges RESTART IDENTITY """))
            
            conn.execute(text(""" INSERT INTO src.crypto_exchanges(name) 
                              
                              select name from src.tmp_crypto_exchanges
                              
                              ) """))
            
            conn.execute(text("""drop table src.tmp_crypto_exchanges """ ))
            
            
            logger.info("crypto exchanges etl completed. Rows : %s", len(df))
            
            
    except Exception:
        logger.exception("Crypto Currencies Exchanges etl failed")


            