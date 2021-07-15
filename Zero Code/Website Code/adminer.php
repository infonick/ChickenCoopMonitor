<?php
function adminer_object() {
    include_once "./plugins/plugin.php";
    include_once "./plugins/login-password-less.php";
    return new AdminerPlugin(array(
        // TODO: inline the result of password_hash() so that the password is not visible in source codes
        new AdminerLoginPasswordLess(password_hash("admin", PASSWORD_DEFAULT)),
    ));
}
include "./adminer-4.8.1-en.php";
