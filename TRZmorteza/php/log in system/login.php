<?php

function is_logged_in() {
    return isset($_SESSION['user_id']);
    }
    
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login_btn'])) {
        session_start(); // must be at top
        $_SESSION['user_id'] = 1;
}


if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['logout_btn'])) {
    unset($_SESSION['user_id']);
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Example</title>
</head>
<body>

<?php if(is_logged_in()): ?>
    <h1>You are logged in</h1>
    <form method="POST">
        <button type="submit" name="logout_btn">Log out</button>
    </form>
<?php else: ?>
    <h1>You are not logged in</h1>
    <form method="POST">
        <button type="submit" name="login_btn">Log in</button>
    </form>
<?php endif; ?>

</body>
</html>