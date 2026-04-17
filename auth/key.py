import secrets

SECRET_KEY = secrets.token_urlsafe(32)
print("Generated SECRET_KEY:", SECRET_KEY)