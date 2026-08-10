
SELECT 
ticker
,company_name
,sector
,industry
,country
,city
,exchange
,currency
,website
,employee_count:: bigint as employee_count
FROM {{ source('src', 'company') }}