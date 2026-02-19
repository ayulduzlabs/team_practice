<?php
function calculate_weekly_pay($hour, $rate):int{//return type hinting
    if ($hour <= 40) {
        return $hour * $rate;
    } else {
        $overtime_hours = $hour - 40;
        return (40 * $rate) + ($overtime_hours * $rate * 1.5);
    }
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $hour = $_POST['hour'];
    $rate = 15;
    $weekly_pay = null;

    
}
// if ($_SERVER['REQUEST_METHOD'] === 'GET') {
//     echo "please enter your hour and rate to calculate your weekly pay";
    
// }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <?php if ($_SERVER['REQUEST_METHOD'] === 'GET'): ?>
        <form action="" method="post">
            <input type="number" name="hour" placeholder="enter your hour"><br>
            <input type="text" name="name" placeholder="enter your name"><br>
            <button type="submit">calculate</button>
        </form>
    <?php endif; ?>
    <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
       <?php 
        $name = $_POST['name'];
        echo "hello {$name} ";
        echo calculate_weekly_pay($hour, $rate); ?> this week.</p>
    <?php endif;?>
</body>
</html>