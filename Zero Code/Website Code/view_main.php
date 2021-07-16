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
	

	//SENSOR FUNCTIONS ------------------------------------------------------
    function getSensorData(){
        console.log('starting getSensorData function');
        var data = {page: "Main", command: "getSensorData"};
        var url = 'controller.php';
        $.post(url, data, sensorTable);
	}

    function sensorTable(data){
        console.log(data);
        data = JSON.parse(data);

        var htmlOut = "<div class='row'><table class='table'>";
        htmlOut += "<tr><th>Sensor Name</th><th>Sensor Data</th></tr>";
		sortedData = [];
		for (var key in data){
			sortedData.push(key);
		}
		sortedData.sort();
        for (let i = 0; i < sortedData.length; i++){
            htmlOut += "<tr><th>";
            htmlOut += sortedData[i];
            htmlOut += "</th><th>";
            if (data[sortedData[i]].constructor == Object) {
                for (var subkey in data[sortedData[i]]){
                    htmlOut += subkey + ": " + data[sortedData[i]][subkey];
                    htmlOut += "<br>";
                }
            }
            else {
                htmlOut += data[sortedData[i]];
            }
            htmlOut += "</th></tr>";
        }
        htmlOut += "</table></div>";

        $('#mainSection').html(htmlOut);
        setTimeout(getSensorData, 2000);
    }

    getSensorData()


});
</script>

