import pandas as pd
from sqlalchemy import text
from etl.database import get_engine


def load_tickers():
    engine = get_engine()

    tickers = pd.DataFrame([
        {"ticker": "AAPL", "category": "Technology"},
        {"ticker": "MSFT", "category": "Technology"},
        {"ticker": "NVDA", "category": "AI / Semiconductors"},
        {"ticker": "AMZN", "category": "E-Commerce / Cloud"},
        {"ticker": "GOOGL", "category": "AI / Advertising"},
        {"ticker": "META", "category": "Social Media / AI"},
        {"ticker": "TSLA", "category": "EV / Energy"},
        {"ticker": "AVGO", "category": "Semiconductors"},
        {"ticker": "COST", "category": "Retail"},
        {"ticker": "NFLX", "category": "Streaming"},
        {"ticker": "AMD", "category": "Semiconductors"},
        {"ticker": "INTC", "category": "Semiconductors"},
        {"ticker": "ADBE", "category": "Software"},
        {"ticker": "PEP", "category": "Consumer Defensive"},
        {"ticker": "CSCO", "category": "Networking"},
        {"ticker": "ORCL", "category": "Cloud / Database"},
        {"ticker": "CRM", "category": "Software / CRM"},
        {"ticker": "IBM", "category": "Technology"},
        {"ticker": "QCOM", "category": "Semiconductors"},
        {"ticker": "TXN", "category": "Semiconductors"},
        {"ticker": "ASML", "category": "Semiconductor Equipment"},
        {"ticker": "MU", "category": "Memory Chips"},
        {"ticker": "SHOP", "category": "E-Commerce"},
        {"ticker": "PYPL", "category": "FinTech"},
        {"ticker": "UBER", "category": "Transportation"},
        {"ticker": "ABNB", "category": "Travel"},
        {"ticker": "SNOW", "category": "Cloud Data"},
        {"ticker": "PLTR", "category": "AI / Analytics"},
        {"ticker": "CRWD", "category": "Cybersecurity"},
        {"ticker": "PANW", "category": "Cybersecurity"},
        {"ticker": "NOW", "category": "Enterprise Software"},
        {"ticker": "ARM", "category": "Semiconductors"},
        {"ticker": "SAP", "category": "Enterprise Software"},
        {"ticker": "DIS", "category": "Entertainment"},
        {"ticker": "KO", "category": "Consumer Defensive"},
        {"ticker": "FROG","category":"AI / Cyber Security"},
        {"ticker": "HOOD","category":"AI / Fintech"},
        {"ticker": "THNQ","category":"AI / Analytics"},
        {"ticker": "WTAI","category":"AI / Thematic Technology"},
        {"ticker": "AIQ","category": "AI / Hardware Technologies"},
        {"ticker": "NBIS","category":"AI"},
        {"ticker": "RYTM", "category": "Biotechnology"},
        {"ticker": "LNTH", "category": "Biotechnology / Renewable Energy"},
        {"ticker": "ABCL", "category": "Biotechnology"},
        {"ticker": "MP", "category": "Chips / Nanotechnology"},
        {"ticker": "ABAT", "category": "Chips / Nanotechnology / EV"},
        {"ticker": "TSM", "category": "Chips / Nanotechnology"},
        {"ticker": "BE", "category": "Renewable Energy"},
        {"ticker": "UUUU", "category": "Renewable Energy"},
        {"ticker": "IBLC", "category": "Blockchain"},
        {"ticker": "VSAT", "category": "Rare Elements / Space"},
        {"ticker": "USAR", "category": "Rare Elements"},
        {"ticker": "TMC", "category": "Rare Elements"},
        {"ticker": "LAC", "category": "Rare Elements"},
        {"ticker": "TMQ", "category": "Rare Elements"},
        {"ticker": "NB", "category": "Rare Elements"},
        {"ticker": "AREC", "category": "Rare Elements"},
        {"ticker": "IDR", "category": "Rare Elements"},
        {"ticker": "METC", "category": "Rare Elements"},
        {"ticker": "IPX", "category": "Rare Elements"},
        {"ticker": "QBTS", "category": "Space"},
        {"ticker": "GSAT", "category": "Space"},
        {"ticker": "IRDM", "category": "Space"},
        {"ticker": "LUNR", "category": "Space"},
        {"ticker": "NN", "category": "Space"},
        {"ticker": "ECHO", "category": "Space"},
        {"ticker": "RKLB", "category": "Space"},
        {"ticker": "PL", "category": "Space"},

    ])

    with engine.begin() as conn:
        for _, row in tickers.iterrows():
            conn.execute(
                text("""
                    INSERT INTO src.tickers (ticker, category)
                    VALUES (:ticker, :category)
                    ON CONFLICT (ticker) DO NOTHING
                """),
                {
                    "ticker": row["ticker"],
                    "category": row["category"]
                }
            )

    print("Tickers loaded successfully.")