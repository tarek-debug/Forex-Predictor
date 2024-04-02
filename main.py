import sys
import os

# Add the flask_user_authentication directory to the Python module search path
project_dir = os.path.dirname(os.path.abspath(__file__))
flask_user_authentication_dir = os.path.join(project_dir, "flask_user_authentication")
sys.path.append(flask_user_authentication_dir)

# Now import the Flask application
from app import app

if __name__ == "__main__":
    app.run(debug=True)
