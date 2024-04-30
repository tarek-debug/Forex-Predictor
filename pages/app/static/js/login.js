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
        if (data.success) {
            showNotification("Login successful. Redirecting...", true);
            setTimeout(function() {
                window.location.href = '/'; // Redirect to the homepage route
            }, 2000); // Redirect after 2 seconds to give user time to read the notification
        } else {
            showNotification("Login failed. Please try again.", false);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        showNotification("An error occurred. Please try again.", false);
    });
}


function register() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    if (password !== confirmPassword) {
        showNotification("Passwords do not match!", false);
        return;
    }

    const data = { username, password };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message || "Registration successful. Please log in.", true);
            showLogin(); // Automatically switch back to login form on successful registration
        } else {
            showNotification(data.error || "Registration failed.", false);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        showNotification("Registration error. Please try again.", false);
    });
}


function showNotification(message, success) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = success ? "#4CAF50" : "#f44336"; // Green for success, red for error
    notification.classList.add('show');

    // After 3 seconds, fade out
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.classList.remove('show');
            notification.style.opacity = '1'; // Reset opacity for next time
        }, 600); // matches transition time
    }, 3000);
}
