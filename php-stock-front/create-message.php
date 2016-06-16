<?php

/*
php -S localhost:9000 -t "C:\storage\code\container-factory-stock\php-front"
Creates one message, unless an integer is specified for Beast Mode, in this case multiple messages are created.
I am having an issue with this and large numbers, process times out after 30 seconds (140ish messages are created).
*/

require_once 'vendor\autoload.php';
use WindowsAzure\Common\ServicesBuilder;

$connectionString = '<queue connection string>';
$queueRestProxy = ServicesBuilder::getInstance()->createQueueService($connectionString);
$queue = "myqueue";

$symbols = trim($_POST['symbols']);
$email = trim($_POST['email']);
$beast = trim($_POST['beast']);

if ($beast) {
    
    $num = (int)$beast;
    
    for ($x = 0; $x <= $num; $x++) {
        $queueRestProxy->createMessage($queue , "$symbols".":"."$email");
    }
          
} else {
    $queueRestProxy->createMessage($queue,"$symbols");
}

?> 