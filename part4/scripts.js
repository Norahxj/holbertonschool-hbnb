document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');
      const errorMessage = document.getElementById('error-message');

      const email = emailInput.value.trim();
      const password = passwordInput.value.trim();

      if (errorMessage) {
        errorMessage.textContent = '';
      }

      try {
        await loginUser(email, password);
      } catch (error) {
        if (errorMessage) {
          errorMessage.textContent = error.message;
        } else {
          alert(error.message);
        }
      }
    });
  }
});

async function loginUser(email, password) {
  const API_URL = '/api/v1/auth/login';

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    let errorText = 'Login failed';

    try {
      const errorData = await response.json();
      errorText = errorData.error || errorData.message || 'Invalid email or password';
    } catch (e) {
      errorText = `Login failed: ${response.statusText}`;
    }

    throw new Error(errorText);
  }
}
