from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('home.html')

@app.route('/history')
def history():
    return render_template('history.html')

# You can add more routes here
@app.route('/login', methods=['POST'])
def login():
    # Your logic to verify username and password
    pass

@app.route('/register', methods=['POST'])
def register():
    # Your logic to register new user and check for unique username and email
    pass
