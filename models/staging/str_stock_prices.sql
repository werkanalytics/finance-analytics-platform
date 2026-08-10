select
    ticker,
    price_date::date as price_date,
    open_price::numeric as open_price,
    high_price::numeric as high_price,
    low_price::numeric as low_price,
    close_price::numeric as close_price,
    volume::bigint as volume
from {{ source('src', 'stock_prices') }}