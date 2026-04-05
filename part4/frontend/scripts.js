document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            console.log("Starting login request");
            console.log("Email:", email);
            console.log("Password:", password);

            const url = "http://127.0.0.1:5000/api/v1/auth/login";

            console.log("Request URL:", url);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                console.log("Response Status:", response.status);
                console.log("Response OK:", response.ok);

                const rawText = await response.text();
                console.log("Raw Response Text:", rawText);

                if (response.ok) {
                    let data;
                    try {
                        data = JSON.parse(rawText);
                    } catch (jsonError) {
                        console.error("JSON Parse Error:", jsonError);
                        alert("Error: Server returned invalid JSON");
                        return;
                    }

                    console.log("Token Received:", data.access_token);

                    document.cookie = `token=${data.access_token}; path=/`;

                    console.log("Redirecting to index.html");
			 window.location.href = "index.html";
                } else {
                    console.error("Login failed. Status:", response.status);
                    alert("Login failed. Status: " + response.status);
                }
            } catch (error) {
                console.error("Fetch Error:", error);
                alert("Error connecting to server: " + error);
            }
        });
    }
});
