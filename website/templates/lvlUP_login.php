<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$username = $_POST['email'];
	$password = $_POST['password'];
	
	// Check if the email exists in the database or file
	// ...
	
	// Verify the password
	if (password_verify($password, $hashed_password)) {
		// Password is correct, store user data in session
		$_SESSION['email'] = $email;
		
		// Redirect to the user's dashboard or another page
		header('Location: lvlUP_account.html');
		exit();
	} else {
		// Password is incorrect, show error message
		echo "Invalid email or password";
	}
}
?>