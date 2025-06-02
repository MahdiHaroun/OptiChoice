import requests

def get_jwt_tokens(username, password):
    try:
        response = requests.post(
            'http://127.0.0.1:8000/auth/jwt/create/',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"JWT error: {e}")
    return None



