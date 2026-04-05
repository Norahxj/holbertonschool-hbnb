// Handle login functionality using backend API

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("http://127.0.0.1:5000/api/auth", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();

                    // Store JWT token in cookie
                    document.cookie = `token=${data.access_token}; path=/`;

                    // Redirect to main page
                    window.location.href = "index.html";
                } else {
                    alert("Login failed: Invalid email or password");
                }

            } catch (error) {
                console.error("Error:", error);
                alert("Error connecting to server");
            }
        });
    }
});
