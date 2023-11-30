function submitForm() {
    // Get form data
    var username = $('#username').val();
    var email = $('#email').val();
    var password = $('#password').val();

    // Create data object
    var formData = {
        username: username,
        email: email,
        password: password
    };

    // Send data to Flask using AJAX
    $.ajax({
        type: 'POST',
        url: '/signup',  // Flask route for signup
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(formData),
        success: function (response) {
            // Handle success, e.g., redirect to a new page
            window.location.href = response.redirect;
        },
        error: function (error) {
            // Handle error
            console.error('Error:', error);
        }
    });
}
