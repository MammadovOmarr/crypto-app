from app import app


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_crypto_price_route(client):
    response = client.get('/crypto_price')
    assert response.status_code == 200
    assert b'Crypto Prices' in response.data

def test_invalid_route(client):
    response = client.get('/invalid_route')
    assert response.status_code == 404

def test_coin_api_bitcoin(client):
    response = client.get('/api/coin/bitcoin')
    assert response.status_code == 200
    assert b'Bitcoin' in response.data

def test_coin_api_ethereum(client):
    response = client.get('/api/coin/ethereum')
    assert response.status_code == 200
    assert b'Ethereum' in response.data

def test_coin_api_solana(client):
    response = client.get('/api/coin/solana')
    assert response.status_code == 200
    assert b'Solana' in response.data

def test_coin_api_invalid(client):
    response = client.get('/api/coin/invalidcoin')
    assert response.status_code == 404