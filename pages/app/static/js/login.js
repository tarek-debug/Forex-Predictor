function showRegistration() {
  document.getElementById('loginForm').style.display = 'none';
  document.getElementById('registrationForm').style.display = 'block';
}

function showLogin() {
  document.getElementById('registrationForm').style.display = 'none';
  document.getElementById('loginForm').style.display = 'block';
}

function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const data = { username, password };

  fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

function register() {
  const username = document.getElementById('regUsername').value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;
  const confirmPassword = document.getElementById('regConfirmPassword').value;

  if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
  }

  const data = { username, email, password };

  fetch('/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      console.log('Registration Success:', data);
      showLogin(); // Automatically switch back to login form on successful registration
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}
