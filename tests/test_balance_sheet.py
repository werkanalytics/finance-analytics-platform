import pytest
from etl.balance_sheet import validate_balance_sheet



def test_valid_balance_sheet():
     row = {
            "ticker": "AAPL",
            "metric_name": "Total Assets",
            "report_date": "2025-12-31",
            "metric_value": 1000000
        }
     assert validate_balance_sheet(row) is True
     
     
def test_empty_ticker():
    row = {
        "ticker":"",
        "metric_name":"Total Assets",
        "report_date": "2025-12-31",
        "metric_value": 1000000
        
    }
    
    with pytest.raises(ValueError):
        validate_balance_sheet(row=row)
        
    


         
    
    
     
     
     
     
     
    
    