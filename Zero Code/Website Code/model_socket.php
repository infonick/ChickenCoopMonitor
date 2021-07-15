<?php
error_reporting(E_ALL);


function socketRequest($message){
    $businessLogicSocketAddr = "localhost";
    $businessLogicPort = 50000;
    
    if (($socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP)) == false) {
        echo "socket_create() failed: " . socket_strerror(socket_last_error()) . "\n";
        return false;
    }

    socket_set_option($socket, SOL_SOCKET, SO_SNDTIMEO, array('sec' => 1, 'usec' => 0));
    socket_set_option($socket, SOL_SOCKET, SO_RCVTIMEO, array('sec' => 1, 'usec' => 0));

    if (($s = socket_connect($socket, $businessLogicSocketAddr, $businessLogicPort)) == false) {
        echo "socket_connect() failed: " . socket_strerror(socket_last_error($socket)) . "\n";
        return false;
    }

    $msgLength = strlen($message);

    $result = socket_write($socket, $message, $msgLength);

    if ($result == false) {
        echo "socket_write() failed: " . socket_strerror(socket_last_error($socket)) . "\n";
        return false;
    }
    else if ($result < $msgLength) {
        echo "socket_write() did not write all data. " . $msgLength . " in buffer, " . $result . " written.\n";
        return false;
    }
    
    /*
    while ($out = socket_read($socket, 2048)) {
        $out = json_decode($out);
        foreach ($out as $key => $value) {
            echo $key . ' : ' . $value . "<br>";
        }
    }*/

    $out = socket_read($socket, 2048);
    //$out = json_decode($out);

    socket_shutdown($socket, 2);
    socket_close($socket);

    return $out;
}


?>