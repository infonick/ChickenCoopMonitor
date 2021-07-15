<?php
//START PHP SESION
if (session_status() == PHP_SESSION_NONE){
	session_start();
}

//INITIALIZE VARIABLES ****************************************************************************
//For Controller
$_POST['page'] = (empty($_POST['page'])) ? "" : $_POST['page'];
$command = (empty($_POST['command'])) ? "" : $_POST['command'];

//For Login page
$usernameError = False;
$passwordError = False;
$newUsernameError = False;
$newPasswordError = False;
$newEmailError = False;
$signupError = False;

$recoveryUsernameError = False;
$recoveryAnswerError = False;
$recoveryPasswordError = False;

//For Main page



//REQUIRED RESOURCES ******************************************************************************
require('model.php');
require('model_socket.php');



//Controller Functions ****************************************************************************
//check and format an input value for security
function checkInput ($value){
	$value = trim($value);
	$value = stripslashes($value);
	$value = htmlspecialchars($value);
	$value = addslashes($value);
	return $value;
}


//test if a password meets strength requirements. At this time, the return string is not strictly in use - the code is being saved for later.
function passwordStrength ($p) {
	$returnArray = array();
	if (strlen($p) < 8)
		array_push($returnArray, "more than 8 characters");

	if (preg_match("~[a-z]+~",$p) != 1)
		array_push($returnArray, "a lowercase character (a-z)");

	if (preg_match("~[A-Z]+~",$p) != 1)
		array_push($returnArray, "an uppercase character (A-Z)");

	if (preg_match("~[0-9]+~",$p) != 1)
		array_push($returnArray, "at least one number (0-9)");
	
	/*$returnString = "";
	if (count($returnArray) > 0){
		$returnString .= "Password must contain ";
		for ($i = 0; $i < count($returnArray); $i++){
			$returnString .= $returnString[$i];
			if ((count($returnArray) - $i) > 2) $returnString .= ", ";
			else if ((count($returnArray) - $i) == 2) $returnString .= " and ";
		}
		$returnString .= ".";
	}*/
	
	return count($returnArray);//return a number to represent true/false
}


//Test if email address is of a valid format
function emailTest($e){
	if (filter_var($e, FILTER_VALIDATE_EMAIL))
		return true;
	else return false;
}


//Exit the controller
function terminate(){
	closeDBConnection();
	exit();
}


//CONTROLLER LOGIC ********************************************************************************
// When commands come from the 'Login' page

if ($_POST['page'] == 'Index')
{
	switch($command) {
		case 'SignIn':
			if (!user_verified($_POST['username'], $_POST['current-password'])) {
				if (!user_exists($_POST['username'])) $usernameError = True;
				else $passwordError = True;
				include('view_login.php');
			}
			
			else {
				openSession($_POST['username']);
				include('view_main.php');
			}
			break;


		case 'NewUser':

			if (user_exists($_POST['new-username']))
				$newUsernameError = True;
			if (passwordStrength($_POST['new-password']))
				$newPasswordError = True;
			if (!emailTest($_POST['new-email']))
				$newEmailError = True;
			
			if ($newUsernameError || $newPasswordError || $newEmailError) {
				include('view_login.php');
			}
            
			else if (add_user($_POST['new-username'], 
                              $_POST['new-name'], 
                              $_POST['new-password'], 
                              $_POST['new-email'],
                              $_POST['new-recoveryQuestion'], 
                              $_POST['new-recoveryAnswer'])) {
				openSession($_POST['new-username']);
				include('view_main.php');
			}
			else {
				$signupError = True;
				include('view_login.php');
			}
			break;

		case 'recoveryUsernameSubmit':
			if (!user_exists($_POST['rUsername'])){
				echo False;
				break;
			}
			else {
				echo get_user_recovery_question($_POST['rUsername']);
				break;
			}
		
		case 'passwordReset':
			if (!user_exists($_POST['rUsername'])){
				echo json_encode('badUsername');
				break;
			}
			else if (!user_recovery_question_verified($_POST['rUsername'], $_POST['rAnswer'])) {
				echo json_encode('badAnswer');
				break;
			}
			else if (passwordStrength($_POST['rPassword'])) {
				echo json_encode('badPassword');
				break;
			}
			else {
				openSession($_POST['rUsername']);
				changePassword($_POST['rPassword']);
				echo json_encode('success');
				break;
			}
		
		default:
			include('view_login.php');
			break;
	}
	
	terminate();
}


// When commands come from the 'Main' page, or when an active session is already in place
else if (($_POST['page'] == 'Main') || (isset($_SESSION["Username"])))
{
	if (!isset($_SESSION['Username'])) {
		session_unset();
		session_destroy();
		include('view_login.php');
	}
	
	else if ($command == ""){
		include('view_main.php');
	}

	else switch($command) {
			
		case 'ChangePassword':
			if (passwordStrength($_POST['password']))
				echo False;
			else echo changePassword($_POST['password']);
			break;
			
		case 'ChangeEmail':
			if (!emailTest($_POST['newEmail']))
				echo False;
			else echo changeEmail($_POST['oldEmail'], $_POST['newEmail']);
			break;
		
		case 'GetEmail':
			echo json_encode(get_user_emails());
			break;
			
		case 'UnsubscribeUser':
			echo unsubscribeUser();
			break;
			
        case "getSensorData":
            echo socketRequest("request");
            break;
		
		case "chickenDoorOpen":
			socketRequest("chickenDoorOpen");
			echo True;
			break;
        
		case "chickenDoorAuto":
			socketRequest("chickenDoorAuto");
			echo True;
			break;
		
		case "cameraLEDToggle":
			socketRequest("cameraLEDToggle");
			echo True;
			break;

		case "cameraLEDOn":
			socketRequest("cameraLEDOn");
			echo True;
			break;

		case "cameraLEDOff":
			socketRequest("cameraLEDOff");
			echo True;
			break;


		case 'LoadCamera':
			include ('view_camera.php');
			break;
			
		case 'LoadDoorOverride':
			include ('view_chickendoor.php');
			break;

		case 'EditProfile':
			include ('view_profile.php');
			break;
		
		case 'SignOut':
			session_unset();
			session_destroy();
			include ('view_login.php');
			break;
	}
	terminate();
}




// When no page is sent from the client and no session exists, send user to the login page

else {
	include ('view_login.php');
	terminate();
}


?>
