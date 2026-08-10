import pandas as pd
import yfinance as yf
from sqlalchemy import text

from etl.database import get_engine


def load_company():
    engine = get_engine()

    tickers_df = pd.read_sql(
        "SELECT ticker FROM src.tickers",
        engine
    )

    tickers = tickers_df["ticker"].tolist()
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

            print(f"{symbol} tamamlandı")

        except Exception as e:
            print(f"{symbol} hata: {e}")

    company_df = pd.DataFrame(company_rows)

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

    print("Company data loaded successfully.")