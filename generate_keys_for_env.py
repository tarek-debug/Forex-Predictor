import secrets
print(secrets.token_urlsafe(16))  # Generates a secure token. You can use this for SECRET_KEY.
print(secrets.token_urlsafe(16))  # Run again for a different value. Use this for CSRF_SECRET_KEY.
