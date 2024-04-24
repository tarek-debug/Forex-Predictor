from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('login.html')

# You can add more routes here
@app.route('/login', methods=['POST'])
def login():
    # Your logic to verify username and password
    pass

@app.route('/register', methods=['POST'])
def register():
    # Your logic to register new user and check for unique username and email
    pass
