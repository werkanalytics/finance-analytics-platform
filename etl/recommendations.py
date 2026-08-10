import pandas as pd
import yfinance as yf
from sqlalchemy import text

from etl.database import get_engine


def load_recommendations():
    engine = get_engine()

    tickers_src = pd.read_sql(
        "SELECT ticker FROM src.tickers",
        engine
    )

    tickers = tickers_src["ticker"].tolist()
    recommendation_rows = []

    for symbol in tickers:
        try:
            rec = yf.Ticker(symbol).recommendations

            if rec is None or rec.empty:
                continue

            rec = rec.reset_index()
            rec["ticker"] = symbol

            recommendation_rows.append(rec)

            print(f"{symbol} recommendations tamamlandı")

        except Exception as e:
            print(f"{symbol} hata: {e}")

    if not recommendation_rows:
        print("Recommendation verisi bulunamadı.")
        return

    recommendations_df = pd.concat(recommendation_rows, ignore_index=True)

    recommendations_df.columns = [
        col.lower().replace(" ", "_") for col in recommendations_df.columns
    ]

    with engine.begin() as conn:
        for _, row in recommendations_df.iterrows():
            conn.execute(
                text("""
                    INSERT INTO src.recommendations (
                        ticker,
                        period,
                        strong_buy,
                        buy,
                        hold,
                        sell,
                        strong_sell
                    )
                    VALUES (
                        :ticker,
                        :period,
                        :strongbuy,
                        :buy,
                        :hold,
                        :sell,
                        :strongsell
                    )
                    ON CONFLICT (ticker, period)
                    DO UPDATE SET
                        strong_buy = EXCLUDED.strong_buy,
                        buy = EXCLUDED.buy,
                        hold = EXCLUDED.hold,
                        sell = EXCLUDED.sell,
                        strong_sell = EXCLUDED.strong_sell
                """),
                row.to_dict()
            )

    print("Recommendations tablosu yüklendi.")