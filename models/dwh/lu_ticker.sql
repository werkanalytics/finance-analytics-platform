SELECT
    md5(upper(trim(ticker))) AS ticker_key,
    upper(trim(ticker)) AS ticker,
    category
FROM {{ ref('slu_tickers') }}