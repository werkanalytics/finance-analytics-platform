SELECT
    md5(ticker) AS ticker_key,
    ticker,
    metric_name,
    report_date,
    metric_value
FROM {{ source('src', 'cash_flow') }}
WHERE metric_value IS NOT NULL