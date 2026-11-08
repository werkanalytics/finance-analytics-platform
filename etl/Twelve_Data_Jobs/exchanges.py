
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import text

from etl.database import get_engine

load_dotenv()

logger = logging.getLogger(__name__)


class TwelveDataClient:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com"

    def get_exchanges(self):

        logger.info("Crypto exchanges ETL started")

        try:
            response = requests.get(
                url=f"{self.base_url}/cryptocurrency_exchanges",
                headers={
                    "Authorization": f"apikey {self.api_key}"
                },
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            if result.get("status") == "error":
                raise RuntimeError(
                    result.get("message", "API hatası")
                )

            df = pd.DataFrame(result["data"])

            if df.empty:
                raise ValueError("API returned empty dataset")

            expected_columns = [
                "id", "name", "code", "country", "timezone"
            ]

            df = df[expected_columns].copy()

            engine = get_engine()

            with engine.begin() as conn:

                df.to_sql(
                    name="tmp_exchanges",
                    con=conn,
                    schema="src",
                    if_exists="replace",
                    index=False
                )

                conn.execute(text("""
                    TRUNCATE TABLE src.exchanges
                    RESTART IDENTITY
                """))

                conn.execute(text("""
                    INSERT INTO src.exchanges
                        (id, name, code, country, timezone)
                    SELECT
                        id, name, code, country, timezone
                    FROM src.tmp_exchanges
                """))

                conn.execute(text("""
                    DROP TABLE src.tmp_exchanges
                """))

            logger.info(
                "Exchanges ETL completed. Rows: %s",
                len(df)
            )

        except requests.exceptions.RequestException:
            logger.exception("HTTP request failed")
            raise

        except (ValueError, RuntimeError, KeyError):
            logger.exception("API response processing failed")
            raise

        except Exception:
            logger.exception("Exchanges ETL failed")
            raise


def load_crypto_exchanges():
    api_key = os.getenv("TWELVE_DATA_KEY")

    if not api_key:
        raise ValueError("API key bulunamadı")

    client = TwelveDataClient(api_key)
    client.get_exchanges()
