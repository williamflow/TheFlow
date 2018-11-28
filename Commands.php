<?php

$json = file_get_contents('php://input');
$post = json_decode($json);
switch ($post->cmd) {
    case "listconnections":
        echo shell_exec("./Flowctl.py listconnections");
        break;
    case "connect":
        shell_exec("./Flowctl.py connect ".escapeshellcmd($post->nodeout)." ".escapeshellcmd($post->nodein));
        break;
    case "disconnect":
        shell_exec("./Flowctl.py disconnect ".escapeshellcmd($post->nodeout)." ".escapeshellcmd($post->nodein));
        break;
}

?>
