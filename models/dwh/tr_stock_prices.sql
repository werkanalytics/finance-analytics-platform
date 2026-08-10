select
    md5(p.ticker) as ticker_key,
    p.ticker,
    p.price_date,
    p.open_price,
    p.high_price,
    p.low_price,
    p.close_price,
    p.volume
from {{ ref('str_stock_prices') }} p