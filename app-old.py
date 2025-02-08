from flask import Flask, request, jsonify
from encryption import encrypt_rating, decrypt_rating, encrypt_aes_key, decrypt_aes_key
import os

app = Flask(__name__)

# Mock Database (Replace with real DB)
database = {}

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json
    player_id = data["player_id"]
    rating = data["rating"]

    # Generate AES key
    aes_key = os.urandom(16)

    # Encrypt rating & AES key
    encrypted_rating = encrypt_rating(rating, aes_key)
    encrypted_aes_key = encrypt_aes_key(aes_key)

    # Save to DB
    database[player_id] = {"rating": encrypted_rating, "aes_key": encrypted_aes_key}

    return jsonify({"message": "Rating submitted successfully"}), 200

@app.route('/get_rating/<player_id>', methods=['GET'])
def get_rating(player_id):
    # Fetch encrypted rating & AES key from DB
    record = database.get(player_id)
    if not record:
        return jsonify({"error": "No rating found"}), 404

    encrypted_rating = record["rating"]
    encrypted_aes_key = record["aes_key"]

    # Decrypt AES key & rating
    aes_key = decrypt_aes_key(encrypted_aes_key)
    decrypted_rating = decrypt_rating(encrypted_rating, aes_key)

    return jsonify({"player_id": player_id, "rating": decrypted_rating}), 200

if __name__ == '__main__':
    app.run(debug=True)
