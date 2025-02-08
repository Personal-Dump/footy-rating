Phase 1
-------

1. Project Setup – Creating a FastAPI project in VS Code.
   * install dependencies
   * create `main.py`
   * run the server
2. Database Models – Defining users, games, ratings, and teams using SQLAlchemy.
   * create `database.py`
   * create `models.py`
   * database migrations - adding models to `migrations/env.py`
3. Authentication – Setting up email-based authentication with JWT.
   * `user` updated in `models.py` to store hashed passwords
   * create `auth.py`
	* connected to SQLite using `sqlite3`
4. Endpoints – Creating APIs for user login, submitting ratings, and getting team suggestions.
5. Email Notifications – Integrating SMTP for sending emails.



Encryption is to be done in areas where sensitive data is stored or transmitted. Key places:

1. *User Authentication*: Store passwords securely (Use hashing, not encryption).
Use AES + RSA to store/reset credentials securely.
2. *Ratings & Feedback Storage*: Encrypt ratings & feedback before saving to the database.
Decrypt only when needed by authorized users.
3. *Emails & Notifications*: Encrypt sensitive email notifications.
4. *Admin Reports & Leaderboards*: Store sensitive reports in encrypted format.




## Running

API running at `http://127.0.0.1:8000`.



SQLite `sqlite3` invoke:
`'C:\Program Files (x86)\SQLite\sqlite3.exe'`
