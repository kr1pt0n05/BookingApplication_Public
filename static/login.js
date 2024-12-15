     // Select the form and error div
    const form = document.getElementById('loginForm');
    const errorDiv = document.getElementById('error');

    // Listen for form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault();  // Prevent default form submission

        // Get the form data
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Create a payload object
        const data = { email, password };

        // Send POST request using fetch API
        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',  // Specify content type as JSON
                },
                body: JSON.stringify(data),  // Convert the data to JSON
            });

            // Handle response based on status codes
            if (response.ok) {
                // If status code is 2xx (success), you can redirect or show success message
                const result = await response.json();
                window.location.replace("/tms");
            } else if (response.status === 400) {
                // Handle specific 400 Bad Request
                const errorData = await response.json();
                errorDiv.textContent = errorData.message || 'Invalid username or password.';
            } else if (response.status === 401) {
                // Handle Unauthorized (e.g., wrong credentials)
                const errorData = await response.json();
                errorDiv.textContent = errorData.message || 'Unauthorized. Please check your credentials.';
            } else if (response.status === 500) {
                // Handle server error
                errorDiv.textContent = 'Server error. Please try again later.';
            } else {
                // For any other status codes, you can display a generic error
                errorDiv.textContent = 'An unexpected error occurred. Please try again.';
            }
        } catch (error) {
            // Catch network or other errors
            errorDiv.textContent = 'An error occurred while trying to login. Please check your connection.';
            console.error('Error during fetch:', error);
        }
    });