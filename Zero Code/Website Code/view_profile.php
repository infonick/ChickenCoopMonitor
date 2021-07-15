<?php
//Load controller, if not already done so.
if (!@include_once('controller.php'))
	exit();
?>


<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta lang="en" />
	<meta name="description" content="Chicken Coop Monitor" />
	<meta name="author" content="Nick Piluso, T00586492" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta charset="utf-8" />
	
	<title>Chicken Coop Monitor</title>
	
	<!-- Bootstrap 4 dependencies -->
	<link rel="stylesheet" href="lib/bootstrap.min.css" />
	
	<!-- Custom CSS -->
	<link rel="stylesheet" href="styles.css" >
</head>


<body>
<!-- SITE HEADER -->
<header class='p-2 pl-3 pr-3 bg-secondary d-flex justify-content-between'>
<!-- Site brand -->
	<span id='brand' class='btn text-white p-0 border-0'>
		<h2 class='d-inline'>Chicken Coop Monitor</h2>
		<!-- site reload form for site brand -->
		<form method='post' action='controller.php' id='pageReload' style='display:none'>
			<input type='hidden' name='page' value='Main'>
			<input type='hidden' name='command' value=''>
		</form>
	</span>
</header>

<!-- SITE NAVIGATION -->
<nav class='p-2 px-3 bg-secondary d-flex justify-content-between'>

<span class="dropdown my-0">
	<button class="btn btn-secondary navbar-dark border my-0 p-1 ml-3" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
		<span class="navbar-toggler-icon"></span>
	</button>
	<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
		<button class='dropdown-item' type="submit" form='loadCamera'>Coop Camera</button>
        <form method='post' action='controller.php' id='loadCamera' style='display:none'>
            <input type='hidden' name='page' value='Main'>
            <input type='hidden' name='command' value='LoadCamera'>
        </form>

		<button class='dropdown-item' type="submit" form='loadDoorOverride'>Doorkeeper Override</button>
		<form method='post' action='controller.php' id='loadDoorOverride' style='display:none'>
			<input type='hidden' name='page' value='Main'>
			<input type='hidden' name='command' value='LoadDoorOverride'>
		</form>
		
        <button class='dropdown-item' type="submit" form='pageReload'>Sensor Readings</button>
		<div class="dropdown-divider"></div>

        <button class='dropdown-item' type="submit" form='loadEditProfile'>Edit Profile</button>
        <form method='post' action='controller.php' id='loadEditProfile' style='display:none'>
            <input type='hidden' name='page' value='Main'>
            <input type='hidden' name='command' value='EditProfile'>
        </form>

        <button class='dropdown-item' type='submit' form='pageSignOut'>Sign Out</button>
        <form method='post' action='controller.php' id='pageSignOut' style='display:none'>
            <input type='hidden' name='page' value='Main'>
            <input type='hidden' name='command' value='SignOut'>
        </form>
        
	
	</div>
    
</span>

<!-- User Greeting -->
    <span class="p-0 m-0 d-flex align-items-center text-white ">
		<span  class='pl-3 pr-3 font-weight-bold' id='welcomeUser'><h4 class='d-inline display-6'>
			Welcome<?php if (isset($_SESSION['Name'])) echo ' ' . $_SESSION['Name'];?></h4>
		</span>
	</span>

</nav>

<!-- Main Website Window-->
<main class='container py-5' id='mainSection'>
	<section class='row'>
	<form method='post' action='controller.php' id='changepassword'>
		<div class="form-group">
			<label class='modal-label' for='new-password'>Enter a new password:</label>
			<p class=''>Minimum 8 characters, must include uppercase, lowercase, and numbers.</p>
			<p class='text-warning' id='newpasswordFeedback'></p>
			<input type='password' class="form-control" name='new-password' id='new-password' autocomplete='new-password'>
		</div>
		<button type="button" class="btn btn-primary" id='submitNewPassword'>Update Password</button>
	</form>
	</section>

	<section class='row py-5'>
	<form method='post' action='controller.php' id='changeemail'>
		<div class="form-group">
			<label class='modal-label' for='current-email'>Current email address:</label>
			<input type='text' class="form-control" name='current-email' id='current-email' disabled>
		</div>
		
		<div class="form-group">
			<label class='modal-label' for='new-email'>Enter a new email address:</label>
			<p class='text-warning' id='newEmailFeedback'></p>
			<input type='email' class="form-control" name='new-email' id='new-email'>
		</div>
		<button type="button" class="btn btn-primary" id='submitNewEmail'>Update Email Address</button>
	</form>
	</section>

	<section class='row'>
	<form method='post' action='controller.php' id='unsubscribe'>
		<div class="form-group">
			<label class='modal-label' for='unsubscribeCheck'>Check the box and click the button to unsubscribe.</label>
			<p class='text-warning' id='unsubscribeFeedback'></p>
			<input type='checkbox' class="form-control" name='unsubscribeCheck' id='unsubscribeCheck'>
		</div>
		<button type="button" class="btn btn-primary" id='submitUnsubscribe' disabled='true'>Unsubscribe</button>
	</form>
	</section>
</main>
<footer>
</footer>
</body>
</html>

<!-- Bootstrap 4 dependencies -->
<script src="lib/jquery-3.5.1.min.js"></script>
<script src="lib/bootstrap.bundle.min.js"></script>

<script>

$(document).ready(function(){
	
	
	//SITE PAGE LOADING --------------------------------------------------
	//Reload the site
	$('#brand').click(function () {
		$('#pageReload').submit();
	});


	$('#submitUnsubscribe').click(function() {
		if ($('#unsubscribeCheck').is(':checked')){
			//console.log("starting..");
			var data = {page: "Main", command: "UnsubscribeUser"};
			var url = 'controller.php';
			$.post(url, data, function(data) {
				//console.log(data);
				if (data) $('#pageSignOut').submit();
				else $('#unsubscribeFeedback').html("Error - please try again.");
			});
		}
		else $('#unsubscribeFeedback').html("Please confirm unsubscribe request by checking the unsubscribe box above.");
	});
	
	$('#unsubscribeCheck').click(function() {
		if ($('#unsubscribeCheck').is(':checked'))
			$("#submitUnsubscribe").attr("disabled", false);
		else
			$("#submitUnsubscribe").attr("disabled", true);
	});
	
	
	$('#submitNewPassword').click(function() {
		//console.log("starting..");
		if ($('#new-password').val() == '')
			$('#newpasswordFeedback').html("Error - please try a different password.");
		var data = {page: "Main", command: "ChangePassword", password: $('#new-password').val()};
		var url = 'controller.php';
		$.post(url, data, function(data) {
			//console.log(data);
			if (data){
				$('#newpasswordFeedback').html("Password successfully changed.");
				$('#new-password').val("");
			}
			else $('#newpasswordFeedback').html("Error - please try a different password.");
		});
	});
	
	
	$('#submitNewEmail').click(function() {
		//console.log("starting..");
		
		var data = {page: "Main", command: "ChangeEmail", oldEmail: $('#current-email').val(), newEmail: $('#new-email').val()};
		var url = 'controller.php';
		$.post(url, data, function(data) {
			//console.log(data);
			if (data){
				$('#newEmailFeedback').html("Email successfully changed.");
				$('#new-email').val("");
				getEmail();
			}
			else $('#newEmailFeedback').html("Error - please check your input and try again.");
		});
	});
	
	function getEmail(){
		var data = {page: "Main", command: "GetEmail"};
		var url = 'controller.php';
		$.post(url, data, function(data) {
			console.log(data);
			if (data) {
				var emails = JSON.parse(data);
				console.log(emails);
				console.log(emails[0]);
				$('#current-email').val(emails[0]);
			}
			else $('#current-email').val("Error");
		});
	}
	
	getEmail();

});
</script>

