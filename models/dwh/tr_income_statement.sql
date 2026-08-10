SELECT
    md5(p.ticker) as ticker_key,
    p.ticker,
    p.report_date,
    p.metric_name,
    p.metric_value
FROM {{ ref('str_income_statement') }} p