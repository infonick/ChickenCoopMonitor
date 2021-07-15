<?php
//Load controller, if not already done so.
if (!@include_once('controller.php'))
	exit();


//DATABASE CONNECTIONS ----------------------------------------------------------------------------
//create DB Connection
$conn = new SQLite3('/var/database/CCMonitor.db');

// Check DB Connection
// if (mysqli_connect_errno())
// echo 'Failed to connect to database: ' . mysqli_connect_error();

//Close DB Connection
function closeDBConnection() {
	global $conn;
	$conn -> close();
}



//DATABASE USER FUNCTIONS -------------------------------------------------------------------------
function user_verified($u, $p) 
{
	global $conn;
	$sql =  "SELECT Password FROM user ";
	$sql .= "WHERE Username = '$u'; ";
	$result = $conn -> querySingle($sql);

	if ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
		return false;
	}
	elseif (password_verify($p, $result))
		return true;
	else
		return false;
}


function user_exists($u) 
{
	global $conn;
	$sql = "SELECT Username FROM user WHERE Username = '$u'";
	$result = $conn -> querySingle($sql);

	if ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
		return false;
	}
	elseif ($result == $u)
		return true;
	else
		return false;
}


function add_user($username, $name, $password, $email, $recoveryQuestion, $recoveryAnswer) 
{
	global $conn;
	
	$date = time();
	$passHash = password_hash($password, PASSWORD_BCRYPT);
	$qaHash = password_hash($recoveryAnswer, PASSWORD_BCRYPT);
	$authCode = 255;
	$acctLock = 0;
	
	//Using transactions to ensure that the whole user profile is added successfully.
	$sql =  "BEGIN TRANSACTION;";
	$sql .= "INSERT INTO user (CreatedDate, Username, Name, Password, AuthCodes, AccountLock) ";
	$sql .=   "VALUES ($date, '$username', '$name', '$passHash', '$authCode', '$acctLock');";
	$sql .= "INSERT INTO user_email (Username, Email) ";
	$sql .=   "VALUES ('$username', '$email');";
	$sql .= "INSERT INTO user_recovery_question (Username, Question, Answer) ";
	$sql .=   "VALUES ('$username', '$recoveryQuestion', '$qaHash');";
	$sql .= "COMMIT;";	

	$success = $conn -> exec($sql);
	
	if ($success) return true;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}



function get_users_name()
{
    global $conn;

	$u = $_SESSION['Username'];
    
	$sql = "SELECT Name FROM user WHERE Username = '$u'";
	$result = $conn -> querySingle($sql);
	if ($result) return $result;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}

function get_user_recovery_question($u)
{
    global $conn;
    
	$sql = "SELECT Question FROM user_recovery_question WHERE Username = '$u'";
	$result = $conn -> querySingle($sql);
	if ($result) return $result;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}

function user_recovery_question_verified($u, $a) 
{
	global $conn;
	$sql =  "SELECT Answer FROM user_recovery_question WHERE Username = '$u'";
	$result = $conn -> querySingle($sql);

	if ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
		return false;
	}
	elseif (password_verify($a, $result))
		return true;
	else
		return false;
}


function get_user_emails() 
{
    global $conn;

	$u = $_SESSION['Username'];
    
    $sql = "SELECT Email FROM user_email WHERE Username = '$u'";
    $result = $conn -> query($sql);
	$out = array();

	if ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
		return false;
	}

    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
		array_push($out, $row['Email']);
	}
    
	return $out;
}


//Open a new session
function openSession($u){
	global $conn;
	
	$_SESSION['Username'] = $u;	
	
	//Get user authorization level and common name
	$sql =  "SELECT AuthCodes, Name FROM user WHERE Username = '$u';";
	$result = $conn -> querySingle($sql, true);
	if ($result){
		$_SESSION['AuthCodes'] = $result['AuthCodes'];
		$_SESSION['Name'] = $result['Name'];
	}
}


//Change User Password
function changePassword($p){
	global $conn;

	$u = $_SESSION['Username'];
	
	$hash = password_hash($p, PASSWORD_BCRYPT);
	$sql = "UPDATE user SET Password = '$hash' WHERE Username = '$u';";
	$result = $conn -> querySingle($sql);

	if ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
		return false;
	}
	else
		return true;
}


//Change User Email Address
function changeEmail($oldEmail, $newEmail){
	global $conn;

	$u = $_SESSION['Username'];
	
	$sql = "UPDATE user_email SET Email = '$newEmail' WHERE Email = '$oldEmail' AND Username = '$u';";

	$success = $conn -> exec($sql);
	
	if ($success) return true;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}


//Delete User Email Address
function deleteEmail($email){
	global $conn;

	$u = $_SESSION['Username'];
	
	$sql = "DELETE FROM user_email WHERE Email = '$email' AND Username = '$u';";

	$success = $conn -> exec($sql);
	
	if ($success) return true;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}


//Unsubscribe a user
function unsubscribeUser(){
	global $conn;

	$u = $_SESSION['Username'];

	$sql =  "BEGIN TRANSACTION;";
	$sql .= "DELETE FROM user_recovery_question WHERE Username = '$u';";
	$sql .= "DELETE FROM user_email WHERE Username = '$u';";
	$sql .= "DELETE FROM user WHERE Username = '$u';";
	$sql .= "COMMIT;";	

	$success = $conn -> exec($sql);
	
	if ($success) return true;
	elseif ($conn -> lastErrorCode()) {
		echo $conn -> lastErrorMsg();
	}
	return false;
}




//DATABASE FUNCTIONS --------------------------------------------------------------------------


?>