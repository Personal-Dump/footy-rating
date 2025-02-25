from flask import Flask, request, jsonify
from encryption import encrypt_rating, decrypt_rating, encrypt_aes_key, decrypt_aes_key
from database import SessionLocal, Rating
from auth import auth_bp  # Import auth routes
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this for production

app.register_blueprint(auth_bp)  # Register authentication routes

@app.route("/")
def home():
    return "Hello, Railway!"

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    try:
        data = request.json
        print("Received Data:", data)  # Debug print

        player_id = data.get("player_id")
        rating = data.get("rating")

        if not player_id or not rating:
            return jsonify({"error": "Missing player_id or rating"}), 400

        # Generate AES key
        aes_key = os.urandom(16)
        print("Generated AES Key:", aes_key)

        # Encrypt rating & AES key
        encrypted_rating = encrypt_rating(rating, aes_key)
        encrypted_aes_key = encrypt_aes_key(aes_key)

        if not encrypted_rating or not encrypted_aes_key:
            return jsonify({"error": "Encryption failed"}), 500

        # Save to DB
        db = SessionLocal()
        new_rating = Rating(
            player_id=player_id,
            rating=rating,  # Save plain rating too (for debugging)
            encrypted_rating=encrypted_rating,
            encrypted_aes_key=encrypted_aes_key
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        db.close()

        return jsonify({"message": "Rating submitted successfully"}), 200
    except Exception as e:
        print("Error:", str(e))  # Print the error in Flask console
        return jsonify({"error": str(e)}), 500

@app.route('/get_rating/<player_id>', methods=['GET'])
def get_rating(player_id):
    try:
        db = SessionLocal()
        record = db.query(Rating).filter(Rating.player_id == player_id).first()
        db.close()

        if not record:
            return jsonify({"error": "No rating found"}), 404

        # Decrypt AES key & rating
        aes_key = decrypt_aes_key(record.encrypted_aes_key)
        decrypted_rating = decrypt_rating(record.encrypted_rating, aes_key)

        return jsonify({"player_id": player_id, "rating": decrypted_rating}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if Railway doesn't provide PORT
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)
