SELECT
ticker,
category
from{{source('src','tickers')}}