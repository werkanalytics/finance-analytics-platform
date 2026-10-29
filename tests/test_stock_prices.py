import pytest

from etl.stock_prices import validate_stock_price

def test_valid_stock_price():
    row = {
        "volume": 1000,
        "high_price": 150,
        "low_price": 120
    }
    
    assert validate_stock_price(row) is True
    

def test_negative_volume():
    row = {
        "volume":-100,
        "high_price":150,
        "low_price":120
    }
    
    with pytest.raises(ValueError):
        validate_stock_price(row)
    

    