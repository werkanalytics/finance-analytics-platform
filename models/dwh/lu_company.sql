SELECT
md5(p.ticker) as ticker_key 
,p.ticker
,p.company_name
,p.sector
,p.industry
,p.country
,p.city
,p.exchange
,p.currency
,p.website
,p.employee_count:: bigint as employee_count
from{{ ref('slu_company') }} p