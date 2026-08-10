SELECT
    md5(p.ticker) AS ticker_key,
    p.ticker,
    p.category,
    p.earnings_date,
    p.eps_estimate,
    p.reported_eps,
    p.surprise_pct
FROM {{ ref('slu_earning_dates') }} p