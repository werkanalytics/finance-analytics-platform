SELECT
md5(id::text) as ID_CRY_CRYPTO_CURR
,symbol as DS_CRY_CRYPTO_SYMBOL
,available_exchanges as DS_CRY_CRYPTO_AVA_EXCH
,currency_base as DS_CRY_BASE_CURRENCY
,currency_quote as DS_CRY_QUOTE_CURRENCY
from {{source('src','crypto_currencies')}}
