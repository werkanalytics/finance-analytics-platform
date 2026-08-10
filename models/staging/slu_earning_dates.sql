SELECT
    e.ticker,
    t.category,
    e.earnings_date,
    e.eps_estimate,
    e.reported_eps,
    e.surprise_pct
FROM {{ source('src', 'earnings_dates') }} e
LEFT JOIN {{ source('src', 'tickers') }} t
    ON e.ticker = t.ticker