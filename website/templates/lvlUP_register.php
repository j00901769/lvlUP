<?php
// Check if the form was submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get the input data from the form
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];
    $user_id = $_POST['user_id'];

    // Validate the input data
    if (empty($username) || empty($email) || empty($password) || empty($confirm_password) || empty($user_id)) {
        // Handle empty fields
        header('Location: signup.php?error=emptyfields');
        exit();
    }
   
    }
    elseif ($password !== $confirm_password) {
        // Handle password mismatch
        header('Location: signup.php?error=passwordmismatch&username=' . $username . '&email=' . $email . '&user_id=' . $user_id);
        exit();
    }

    // Sanitize the input data
    $username = filter_var($username, FILTER_SANITIZE_STRING);
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);
    $user_id = filter_var($user_id, FILTER_SANITIZE_STRING);

    // Generate a hashed password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Store the user data in a database or file
    // Here is just a simple example of storing data in a file
    $user_data = $username . '|' . $email . '|' . $hashed_password . '|' . $user_id . PHP_EOL;
    file_put_contents('users.txt', $user_data, FILE_APPEND);
	
	// Redirect to a success page
	header('Location: lvlUP_success.html');
	exit();
}
?>