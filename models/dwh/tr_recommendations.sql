SELECT
md5(p.ticker) as ticker_key,
p.ticker,
p.period,
strong_buy,
p.buy,
p.hold,
p.sell,
strong_sell
from {{ ref('str_recommendations') }} p