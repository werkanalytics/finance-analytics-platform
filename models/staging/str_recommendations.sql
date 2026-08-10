SELECT
    md5(ticker) AS ticker_key,
    ticker,
    period,
    strong_buy,
    buy,
    hold,
    sell,
    strong_sell
FROM {{ source('src', 'recommendations') }}