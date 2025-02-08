import requests

# Submit a rating
requests.post("http://127.0.0.1:5000/submit_rating", json={"player_id": "123", "rating": 8.5})

# Get the rating
response = requests.get("http://127.0.0.1:5000/get_rating/123")
print(response.json())
