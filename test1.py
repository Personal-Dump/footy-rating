import requests

url = "http://127.0.0.1:5000/submit_rating"
data = {"player_id": "123", "rating": 8.5}

response = requests.post(url, json=data)

# Print raw response content to debug
print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Add this to check for errors