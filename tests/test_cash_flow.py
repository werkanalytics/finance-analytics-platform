import pytest
from etl.cash_flow import validate_cash_flow

def test_valid_cash_flow():
    row = {
        "ticker":"AAPL",
        "metric_name": "Total Assets",
        "report_date": "2025-12-31",
        "metric_value": 1000000
    }
    
    assert validate_cash_flow(row=row) is True
    
def test_empty_ticker():
    row = {
        "ticker":"",
        "metric_name":"Total Assets",
        "report_date": "2025-12-31",
        "metric_value": 1000000
    }
    
    with pytest.raises(ValueError):
        validate_cash_flow(row=row)

