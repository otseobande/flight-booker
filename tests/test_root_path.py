import json

def test_root_path_should_return_welcome_message(client):
    response = client.get('/')
    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body == {
        'message': 'Welcome to Flight booker API'
    }
