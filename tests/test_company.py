import pytest

from etl.company import validate_company


@pytest.fixture
def valid_company():
    return {
        "ticker":"AAPL",
        "company_name":"Apple"
    }

def test_valid_company(valid_company):
    assert validate_company(valid_company) is True
    

def test_empty_ticker(valid_company):
    valid_company["ticker"] = ""
    
    with pytest.raises(ValueError):
        validate_company(valid_company)
        
        
def test_empty_company_name(valid_company):
    valid_company["company_name"] = ""
    
    with pytest.raises(ValueError):
        validate_company(valid_company)
    

    