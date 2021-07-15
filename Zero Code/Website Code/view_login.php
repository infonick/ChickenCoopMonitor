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
	
	<!-- stylesheets -->
	<link rel="stylesheet" href="lib/bootstrap.min.css" />
	<link rel="stylesheet" href="styles.css" />

</head>

<body>
<header class='p-2 pl-3'>
<!-- Site brand -->
	<span id='brand' class='btn text-secondary p-0 border-0'>
		<h2 class='d-inline'>Chicken Coop Monitor</h2>
	</span>

<!-- site reload forms -->
<form method='post' action='controller.php' id='pageReload' style='display:none'>
	<input type='hidden' name='page' value='Index'>
	<input type='hidden' name='command' value=''>
</form>
<form method='post' action='controller.php' id='mainPageReload' style='display:none'>
	<input type='hidden' name='page' value='main'>
	<input type='hidden' name='command' value=''>
</form>
</header>


<main class='container'>
<div class="modal-dialog rounded-0" role="document">
	<!-- Accordion -->
	<div class="accordion modal-content rounded-0 bxshadow" id="loginAccordion">

		<!-- Login Fold -->
		<div class="card rounded-0">
			<div class="card-header p-0" id="loginCard">
				<h2 class="mb-0">
				<button class="btn btn-link btn-block text-left rounded-0 p-3 text-dark" type="button" data-toggle="collapse" data-target="#collapseLoginCard" aria-expanded="true" aria-controls="collapseLoginCard">
				Sign In
				</button>
				</h2>
			</div>

			<div id="collapseLoginCard" class="collapse show" aria-labelledby="loginCard" data-parent="#loginAccordion">
				<div class="card-body bg-secondary text-white">
				<form method='post' action='controller.php'>

					<label class='modal-label' for='username'>Username:</label>
					<?php if ($usernameError) echo "<p class='text-warning'>Invalid username, please try again.</p>"?>
					<input type='text' class="form-control" name='username' required><br>
					<?php if ($passwordError) echo "<p class='text-warning'>Invalid password, please try again.</p>"?>
					<label class='modal-label' for='current-password'>Password:</label>
					<input type='password' class="form-control" name='current-password' autocomplete="current-password" required> <?php if (!empty($error_msg_password)) echo $error_msg_password; ?><br>

					<div class='row justify-content-center'>
						<div class='col-auto m-2'>
							<input type='submit' class='btn btn-light' value='Sign In'>
						</div>
						<div class='col-auto m-2'>
							<input type='reset' class='btn btn-light' value='Clear'>
						</div>
					</div>
					<input type='hidden' name='page' value='Index'>
					<input type='hidden' name='command' value='SignIn'>
				</form>
				</div>
			</div>
		</div>
		

		<!-- Password Recovery Fold -->
		<div class="card rounded-0">
			<div class="card-header p-0" id="recoveryCard">
				<h2 class="mb-0">
				<button class="btn btn-link btn-block text-left rounded-0 p-3 text-dark" type="button" data-toggle="collapse" data-target="#collapseRecoveryCard" aria-expanded="true" aria-controls="collapseRecoveryCard">
				Account Recovery
				</button>
				</h2>
			</div>

			<div id="collapseRecoveryCard" class="collapse" aria-labelledby="recoveryCard" data-parent="#loginAccordion">
				<div class="card-body bg-secondary text-white">
				<form method='post' action='controller.php' id='recoveryUsernameForm'>
				
					<label class='modal-label' for='recovery-username'>Username:</label>
					<p class='text-warning d-none' id='recoveryUsernameFeedback'>Invalid username, please try again.</p>
					<input type='text' class="form-control" name='recovery-username' id='recovery-username' required><br>
					
					<div class='row justify-content-center'>
						<div class='col-auto m-2'>
							<input type='button' class='btn btn-light' value='Submit' id='recoveryUsernameSubmit'>
						</div>
						<div class='col-auto m-2'>
							<input type='reset' class='btn btn-light' value='Clear'>
						</div>
					</div>
					<input type='hidden' name='page' value='Index'>
					<input type='hidden' name='command' value='recoverAccount'>
            	</form>

				<form class='d-none' method='post' action='controller.php' id='resetPasswordForm'>
					<input type='hidden' class="form-control" name='recovery-username2' id='recovery-username2' required><br>

					<p class='' id='RecoveryQuestion'></p>

					<label class='modal-label' id='recovery-answer-label' for='recovery-answer'>Answer:</label>
					<p class='text-warning d-none' id='recoveryAnswerFeedback'>Invalid answer, please try again.</p>
					<input type='text' class="form-control" name='recovery-answer' id='recovery-answer' disabled='true' required><br>
					
					<label class='modal-label' id='recovery-password-label' for='recovery-password'>Enter a new password:</label>
					<p class='' id='recovery-password-instructions'>Minimum 8 characters, must include uppercase, lowercase, and numbers.</p>
					<p class='text-warning d-none' id='recoveryPasswordFeedback'>Invalid password, please try a different one.</p>
					<input type='password' class="form-control" name='recovery-password' id='recovery-password' disabled='true' required><br>
					
					<div class='row justify-content-center'>
						<div class='col-auto m-2'>
							<input type='button' class='btn btn-light' value='Submit' id='recoveryPasswordResetSubmit'>
						</div>
						<div class='col-auto m-2'>
							<input type='reset' class='btn btn-light' value='Clear'>
						</div>
					</div>
					<input type='hidden' name='page' value='Index'>
					<input type='hidden' name='command' value='recoverAccount'>
				</form>
				</div>
			</div>
		</div>


		<!-- Sign-Up Fold -->
		<div class="card rounded-0">
			<div class="card-header p-0" id="signupCard">
				<h2 class="mb-0">
				<button class="btn btn-link btn-block text-left rounded-0 p-3 text-dark" type="button" data-toggle="collapse" data-target="#collapseSignupCard" aria-expanded="true" aria-controls="collapsesignupCard">
				Sign Up
				</button>
				</h2>
			</div>

			<div id="collapseSignupCard" class="collapse" aria-labelledby="signupCard" data-parent="#loginAccordion">
				<div class="card-body bg-secondary text-white">
				<form method='post' action='controller.php'>
				
					<?php if ($signupError) echo "<p class='text-warning'>Something went wrong, but maybe try again.</p>"?>

					<label class='modal-label'>Enter a username:</label>
					<p class='text-warning' id='newusernameFeedback'><?php if ($newUsernameError) echo "Invalid username, please try a different one."?></p>
					<input type='text' class="form-control" name='new-username' required><br>
					
					<label class='modal-label' for='new-password'>Enter a password:</label>
					<p class=''>Minimum 8 characters, must include uppercase, lowercase, and numbers.</p>
					<p class='text-warning' id='newpassowrdFeedback'><?php if ($newPasswordError) echo "Invalid password, please try a different one."?></p>
					<input type='password' class="form-control" name='new-password' autocomplete='new-password' required><br>

                    <label class='modal-label'>Enter your first name:</label>
					<input type='text' class="form-control" name='new-name' required><br>

					<label class='modal-label'>Enter your email address:</label>
					<p class='text-warning' id='newEmailFeedback'><?php if ($newEmailError) echo "Invalid email address, please try again."?></p>
					<input type='email' class="form-control" name='new-email' autocomplete='email' required><br>

                    <label class='modal-label'>Enter a password recovery question:</label>
					<input type='text' class="form-control" name='new-recoveryQuestion' required><br>

                    <label class='modal-label'>Enter the answer to the recovery question:</label>
					<input type='text' class="form-control" name='new-recoveryAnswer' required><br>
					
					<div class='row justify-content-center'>
						<div class='col-auto m-2'>
							<input type='submit' class='btn btn-light' value='Sign Up' >
						</div>
						<div class='col-auto m-2'>
							<input type='reset' class='btn btn-light' value='Clear'>
						</div>
					</div>
					<input type='hidden' name='page' value='Index'>
					<input type='hidden' name='command' value='NewUser'>
            </form>
				</div>
			</div>
		</div>


	</div>
</div>

</main>
</body>
</html>

<!-- Bootstrap 4 dependencies -->
<script src="lib/jquery-3.5.1.min.js"></script>
<script src="lib/bootstrap.bundle.min.js"></script>

<script>

	//show section if user previously submitted a request with errors.
	if (<?php if($newUsernameError || $newPasswordError || $newEmailError) echo 'true'; else echo 'false';?>) $('#collapseSignupCard').collapse('show');
	else if (<?php if($recoveryUsernameError || $recoveryAnswerError || $recoveryPasswordError) echo 'true'; else echo 'false';?>) $('#collapseRecoveryCard').collapse('show');

	$('#brand').click(function () {
		$('#pageReload').submit();
	});


	$('#recoveryUsernameSubmit').click(function() {
        //console.log("starting..");
        var data = {page: "Index", command: "recoveryUsernameSubmit", rUsername: $('#recovery-username').val()};
        var url = 'controller.php';
		$('#recovery-username2').val($('#recovery-username').val())
        $.post(url, data, function(data) {
            if(data){
				showPasswordRecoveryForm();
				$('#RecoveryQuestion').html(data + '?');
				$('#recoveryUsernameFeedback').addClass('d-none');
			}
			else {
				hidePasswordRecoveryForm()
				$('#recoveryUsernameFeedback').removeClass('d-none');
			}
        });
	});

	$('#recoveryPasswordResetSubmit').click(function() {
        //console.log("starting.. recoveryPasswordResetSubmit");
        var data = {page: "Index", command: "passwordReset", rUsername: $('#recovery-username').val(), rAnswer: $('#recovery-answer').val(), rPassword: $('#recovery-password').val()};
        var url = 'controller.php';
		$('#recoveryAnswerFeedback').addClass('d-none');
		$('#recoveryPasswordFeedback').addClass('d-none');
        $.post(url, data, function(data) {
			console.log('RECD ' + data);
			data = JSON.parse(data);
			console.log(typeof(data));
            switch (data){
				case "badUsername":
					$("#resetPasswordForm").trigger("reset");
					$("#recoveryUsernameForm").trigger("reset");
					$('#recoveryUsernameFeedback').removeClass('d-none');
					break;

				case "badAnswer":
					$('#recoveryAnswerFeedback').removeClass('d-none');
					break;

				case "badPassword":
					$('#recoveryPasswordFeedback').removeClass('d-none');
					break;
				
				case "success":
					console.log('act-success');
					// $('#mainPageReload').submit();
					// location.reload();
					window.location.href = '/controller.php';
					break;
			}
        });
	});



	function hidePasswordRecoveryForm(){
		$('#resetPasswordForm').addClass('d-none');

		$("#recovery-answer").attr("disabled", true);
		$("#recovery-password").attr("disabled", false);

		$('#recovery-answer').val("");
		$('#recovery-password').val("");
	}

	function showPasswordRecoveryForm(){
		//display-block elements
		$('#resetPasswordForm').removeClass('d-none');

		$("#recovery-answer").attr("disabled", false);
		$("#recovery-password").attr("disabled", false);
	}


</script>