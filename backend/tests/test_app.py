from app import app

def test_generate():
    with app.test_client() as client:
        response = client.get('/generate')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'ok'}
