import json
from sqlalchemy import text
from etl.database import get_engine
import logging
import os
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

logger = logging.getname(__name__)

url = "https://api.twelvedata.com/stocks"

def load_stocks():
    logger.info("stocks etl started")
    
    try:
        api_key = os.getenv("TWELVE_DATA_KEY")
        
        if not api_key:
            raise ValueError("API key cannot be found")
       
        engine = get_engine()
        
        response = requests.get(
            url=url,
            headers={"Authorization": f"apikey {api_key}"},
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "error":
            raise RuntimeError(result.get("message","API Hatası"))
        
        json.dumps(result,indent=4, ensure_ascii=False)
        
        df = pd.DataFrame(result["data"])
        
        if df.empty:
            raise ValueError("API returned empty dataset")
        
        expected_columns = ["id","symbol","name","currency","exchange","country","type"]
        df = df[expected_columns].copy()
        
        
        
        with engine.begin as conn:
            df.to_sql(
            name="tmp_stocks",
            schema="src",
            if_exists="replace",
            index=False
            )
            
            
            conn.execute(text(""" TRUNCATE TABLE src.stocks RESTART IDENTITY """))
            
            conn.execute(text(""" INSERT INTO src.stocks 
                             SELECT  id
                                    ,symbol
                                    ,name
                                    ,currency
                                    ,exchange
                                    ,country
                                    ,type FROM src.tmp_stocks"""))
            
            conn.executr(text(""" drop table src.tmp_stocks """))
            
            logger.info("stocks etl completed. Rows : %s", len(df))
            
    
    except Exception:
        logger.exception("stocks etl failed")
    


    


