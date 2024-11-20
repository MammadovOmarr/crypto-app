import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Go to Crypto Price Tracker' in response.data 

def test_crypto_price_route(client):
    response = client.get('/crypto_price')
    assert response.status_code == 200
    assert b'<title>Crypto Price Tracker</title>' in response.data  

def test_invalid_route(client):
    response = client.get('/invalid_route')
    assert response.status_code == 404

def test_coin_api_bitcoin(client):
    response = client.get('/api/price/bitcoin') 
    assert response.status_code == 200
    assert b'price_usd' in response.data  

def test_coin_api_ethereum(client):
    response = client.get('/api/price/ethereum')  
    assert response.status_code == 200
    assert b'price_usd' in response.data  

def test_coin_api_solana(client):
    response = client.get('/api/price/solana')  
    assert response.status_code == 200
    assert b'price_usd' in response.data  

def test_coin_api_invalid(client):
    response = client.get('/api/price/invalidcoin') 
    assert response.status_code == 500
    assert b'error' in response.data  
