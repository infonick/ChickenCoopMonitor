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
<!-- MODAL WINDOW -->
<div class="modal fade" id="modal" tabindex="-1" role="dialog" aria-labelledby="modal" aria-hidden="true">
	<div class="modal-dialog rounded-0" role="document">
	 <div class="modal-content rounded-0 bxshadow">
		<div class="modal-header">
			<h5 class="modal-title">Modal title</h5>
			<button type="button" class="close" data-dismiss="modal" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
		</div>
		<div class="modal-body d-flex justify-content-center">
			<div class="spinner-border text-secondary" role="status">
				<span class="sr-only">Loading data..</span>
			</div>
		</div>
		<div class="modal-footer">
			<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
			<button type="button" class="btn btn-primary">Save changes</button>
		</div>
		</div>
	</div>
</div>


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
		<!--button class='dropdown-item' type='button' id='loadDashboard'>Dashboard</button-->
		<!--?php if ($_SESSION['AuthAdminRead']) echo
		"<button class='dropdown-item' type='button' id='loadAdminPanel'>Admin Panel</button>
		<div class='dropdown-divider'></div>";
		?-->
		<!--?php if ($_SESSION['AuthCreateProject']) echo
		"--><!--div class='dropdown-divider'></div-->
		<!--<button class='dropdown-item' type='button' id='loadMyProjects'>My Projects</button>
		<button class='dropdown-item' type='button' id='loadMyTasks'>My Activities & Tasks</button>
		<button class='dropdown-item' type='button' id='newProject'>Start New Project</button>
        <button class='dropdown-item' type='button' id='loadAllProjects'>List All Projects</button>-->
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
	<!--<button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#modal">
	  Launch demo modal
	</button>
	<br><br>-->
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
	
	//Load "New Project" form
	/*$("#newProject").click(function() {
		$("#mainSection").load("view_newJob.txt", function() {
			$('#jobParent').val('NULL'),
			$('#jobAuthLevel').val('1')
		});
	});*/
	
	//Load "Edit Profile" form
	/*$("#loadEditProfile").click(function() {
		$("#mainSection").load("view_editProfile.txt");
	});*/

	//Load "Edit Job" form
	/*$('#mainSection').on('click', '#editJobDetails', function(){
		var jid = $('#JobID').val();
		$("#mainSection").load("view_editJob.txt", function(){
			var input = {
				AND: {
					'PMJob.JID': jid
				},
				OR : {
				}
			};
			input = JSON.stringify(input);
			//console.log(input);
			searchJobFunction(input, showEditJobDetails);
		});
	});*/





	//SEARCH FUNCTIONS AND OPERATIONS ------------------------------------
	//Submit a seach query from the search bar
	/*$('#searchSubmit').click(submitSearch); //create click event for serach button
	
	$("#searchbar").keydown(function(keyVent){ //prevent page from submitting if enter key is pressed
		if (keyVent.which == 13){
			keyVent.preventDefault();
			submitSearch();
		}
	});*/
	
	/*function submitSearch() {
		var searchTerm = $('#searchbar').val();
		var input = {
			AND: {
				
			},
			OR: {
					'PMJobDetail.Name': $('#searchbar').val(),
					'PMJobDetail.Description': $('#searchbar').val()
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, searchSubmitCallback);
	}*/
	
	/*function searchSubmitCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			var result = formatSearchResult(data);
			$('#searchbar').val("");
		}
		else var result = "There are no search results to display.";
		$('#mainSection').html(result);
	};*/


	//Search for this user's projects
	/*$('#loadMyProjects').click(function() {
		var input = {
			AND: {
				'PMUserJob.UID': <?php if (isset($_SESSION['UID'])) echo $_SESSION['UID'];?>,
				'PMJob.ParentJID': 'IS NULL',
				'PMUserJob.DeleteFlag': 'False'
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, loadMyProjectsCallback);
	});
	
	$('#loadMyProjects').trigger('click');*/
	
	/*function loadMyProjectsCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			var result = formatSearchResult(data);
		}
		else var result = "You have no projects to display.";
		$('#mainSection').html(result);
	};*/


//Search for ALL projects
	/*$('#loadAllProjects').click(function() {
		var input = {
			AND: {
				'PMJob.ParentJID': 'IS NULL',
				'PMUserJob.DeleteFlag': 'False'
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, loadMyProjectsCallback);
	});*/
	
	/*function loadMyProjectsCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			var result = formatSearchResult(data);
		}
		else var result = "You have no projects to display.";
		$('#mainSection').html(result);
	};*/


	//Search for this user's tasks
	/*$('#loadMyTasks').click(function() {
		var input = {
			AND: {
				'PMUserJob.UID': <?php if (isset($_SESSION['UID'])) echo $_SESSION['UID'];?>,
				'PMJob.ParentJID': 'IS NOT NULL',
				'PMUserJob.DeleteFlag': 'False'
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, loadMyTasksCallback);
	});*/

	/*function loadMyTasksCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			var result = formatSearchResult(data);
		}
		else var result = "You have no tasks to display.";
		$('#mainSection').html(result);
	};*/


	//Search for a particular job and display it with the callback function
	/*function getJob(jid) {
		//get the job with id=jid
		var input = {
			AND: {
				'PMJob.JID': jid,
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, postJob);
	};*/
	
	/*function getJobCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			if (data[0]['ParentJID'] === null){/*if job 'jid' does not have a parent, return the job as is
				return data;
			}
			else {/*if job 'jid' has a parent, get that job too
				if (parent = getJob(data[0]['ParentJID']))
					return parent.unshift(data[0]);/*put child job infront of parent job
				else return data;
			}
		}
		else return false;
	};*/


	//get all child jobs for job=jid
	/*function getChildJob(jid) {
		//get child jobs with 'parent id'=jid
		var input = {
			AND: {
				'PMJob.ParentJID': jid,
				'PMJobDetail.DeletedDate': 'IS NULL'
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		var data = searchJobFunction(input, getChildJobCallback);
	};*/
	
	/*function getChildJobCallback(data) {
		data = JSON.parse(data);
		if (data.length > 0){
			var result = formatSearchResult(data);
			$('#childSection').html(result);
		}
		//else var result = "There are no " + $('#nextLowerName').html() + "s to display.";
		//$('#childSection').html(result);
	};*/


	//get a parent job to complete the breadcrumb banner
	/*function getBreadcrumb(jid) {
		//get the job with id=jid
		var input = {
			AND: {
				'PMJob.JID': jid,
			},
			OR : {
			}
		};
		input = JSON.stringify(input);
		searchJobFunction(input, postBreadcrumb);
	};*/


	//Core Search Function
	/*function searchJobFunction(searchVars, callBack){
        var data = {page: "Main", command: "SearchJobs", search: searchVars};
        var url = 'controller.php';
		//console.log(data);
        $.post(url, data, callBack);
	}*/


	//Format a list of search results
	/*function formatSearchResult(data){
		var result = "<div class='d-flex justify-content-center flex-wrap'>";
		for (var i = 0; i < data.length; i++) {
			result += "<div class='card cardwidth m-2 bxshadow border-" + data[i]['CategoryColor'] + "'>";
			//result += "<img class='card-img-top bg-" + data[i]['CategoryColor'] + "' alt='No image for " + data[i]['Name'] + "'>"; //NO IMAGE IMPLEMENTED YET
			result += "<div class='card-body'>";
			result += "<h5 class='card-title'>" + data[i]['Name'] + "</h5>";
			result += "<p class='card-text'>" + data[i]['Description'] + "</p>";
			result += "</div>";
			result += "<div class='card-footer border-" + data[i]['CategoryColor'] + "'>";
			result += "<button class='btn btn-" + data[i]['CategoryColor'] + " jobSearchResultButton' value='" + data[i]['JID'] + "'>Open " + data[i]['AuthName'] + "</button>";
			result += "</div></div>";
			//console.log(data[i]);
		}
		result += "</div>";
		return result;
	}*/

	//ADD SEARCH RESULT BUTTON EVENT HANDLER
	/*$('#mainSection').on('click', '.jobSearchResultButton', function(){
		openJob($(this).val());
	});*/


	//JOB FUNCTIONS ------------------------------------------------------
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

	/*function postJob(data) {
		data = JSON.parse(data);
		
		if (data.length > 0){
						
			//Set up breadcrumb header
			var result = "<nav aria-label='breadcrumb'>";
				result += "<ol class='breadcrumb' id='jobBreadcrumbTrail>";
					result += "<li class='breadcrumb-item active' aria-current='page'> " + data[0]['Name'] +" </li>";
				result += "</ol>";
			result += "</nav><br>";
			
			//display job details
			result += "<div class='alert alert-" + data[0]['CategoryColor'] + "' role='alert'><h3 class=''>"+data[0]['Name'];
			result += "<br><small>"+data[0]['Description']+"</small></h3></div>";
			
			result += "<div class='row'>";
			result += "<table class='table'> <tr><th scope='row'>JOB ID:</th><td>"+data[0]['JID']+"</td></tr>";
			result +=						"<tr><th scope='row'>Start Date:</th><td>"+data[0]['StartDate']+"</td></tr>";
			result +=						"<tr><th scope='row'>End Date:</th><td>"+data[0]['EndDate']+"</td></tr></table>";
			result += "<table class='table'> <tr><th scope='row'>Priority:</th><td>"+ priorityToString(data[0]['Priority']) +"</td></tr>";
			result +=						"<tr><th scope='row'>Category:</th><td>"+data[0]['CategoryName']+"</td></tr>";
			result +=						"<tr><th scope='row'>Status:</th><td>"+data[0]['StatusName']+"</td></tr></table>";
			result += "</div>";
			
			result += "<section class='container-fluid py-4 px-0' id='childSection'></section>"; //container for child jobs
			
			$('#mainSection').html(result); //Display the job details into the main section.
			
			getChildJob(data[0]['JID']); //display all child jobs as well.
		}
		else {
			var result = "Job ID " + jid + " does not exist.";
			$('#mainSection').html(result);
		}
		
	};*/

	/*function openJob(jid) {		

		//Set up breadcrumb header
		var result = "<form class='d-none'><input type='hidden' id='JobID' value='"+jid+"'><input type='hidden' id='JobAuthID' value='"+jid+"'></form>";
			result += "<nav aria-label='breadcrumb'>";
			result += "<ol class='breadcrumb alert jobAlertColor' id='jobBreadcrumbTrail'>";
				result += "<li class='breadcrumb-item' aria-current=''>";
				result += "<button class='btn btn-sm jobButtonColor jobName breadcrumb-item' disabled></button></li>";
			result += "</ol>";
		result += "</nav><br>";
		
		//set up job display
		result += "<div class='alert jobAlertColor' id='JobTitleBox' role='alert'><h3 class='jobName'></h3>";
		result += "<h3><small id='JobDescription'></small></h3></div>";
		
		result += "<div class='row'>";
		result += "<table class='table col-sm-6 p-0 m-0'><tr><th class='w-50' scope='row'><Span class='JIDT'>Job</Span> ID:</th><td class='text-left w-50' id='JobIdentifier'>"+jid+"</td></tr>";
		result +=										"<tr><th class='w-50' scope='row'>Start Date:</th>		<td class='text-left w-50' id='JobStartDate'></td></tr>";
		result +=										"<tr><th class='w-50' scope='row'>End Date:</th>		<td class='text-left w-50' id='JobEndDate'></td></tr></table>";
		result += "<table class='table col-sm-6 p-0 m-0'><tr><th class='w-50' scope='row'>Priority:</th>		<td class='text-left w-50' id='JobPriority'></td></tr>";
		result +=										"<tr><th class='w-50' scope='row'>Category:</th>		<td class='text-left w-50' id='JobCategoryName'></td></tr>";
		result +=										"<tr><th class='w-50' scope='row'>Status:</th>			<td class='text-left w-50' id='JobStatusName'></td></tr></table>";
		result += "</div>";
		
		result += "<div class='btn-group btn-group-lg' role='group' aria-label='Options'>";
			result += "<button type='button' class='btn jobButtonColor px-4' id='editJobDetails'>Edit <span class='JIDT'>Details</span></button>";
			result += "<button type='button' class='btn jobButtonColor px-4 d-none' id='createSubtask'>Create <span class='nextLowerName'>Subtask</span></button>";
			//result += "<button type='button' class='btn jobButtonColor px-4' id=''></button>";
		result += "</div>";
		
		result += "<section class='container-fluid py-4 px-0 d-none' id='childSection'>There are no <span class='nextLowerName'>Subtask</span>s to display.</section>"; //container for child jobs
		
		$('#mainSection').html(result); //Display the job details into the main section.
		
		getChildJob(jid); //display all child jobs as well.
		getJob(jid);
	}*/
	
	/*function getJobAuthDetails(auth){
		var data = {page: "Main", command: "GetJobAuthDetails", authLevel: (auth) };
        var url = 'controller.php';
        $.post(url, data, function(data){
			//console.log(data);
			data = JSON.parse(data);
			if(data)$('.nextLowerName').html(data[0]['Name']);
		});
	}*/
	
	/*function postJob(data){
		data = JSON.parse(data);
		
		//var jid = $('#JobID').val();
		//$('#JobID').val(data[0]['JID']);
		color = data[0]['CategoryColor'];
		
		$('.jobAlertColor').addClass("alert-" + color);
		$('.jobButtonColor').addClass("btn-" + color);
		$('#JobIdentifier').html(data[0]['JID']);
		$('#JobDescription').html(data[0]['Description']);
		$('.jobName').html(data[0]['Name']);
		$('#JobStartDate').html(data[0]['StartDate']);
		$('#JobEndDate').html(data[0]['EndDate']);
		$('#JobPriority').html(priorityToString(data[0]['Priority']));
		$('#JobCategoryName').html(data[0]['CategoryName']);
		$('#JobStatusName').html(data[0]['StatusName']);
		$('.JIDT').html(data[0]['AuthName']);
		$('#JobAuthID').val(data[0]['AuthID']);
		if (data[0]['AuthChild'] != '0') {
			$('#createSubtask').removeClass('d-none');
			$('#childSection').removeClass('d-none');
			//console.log("AUthC: " + data[0]['AuthChild']);
			getJobAuthDetails(parseInt(data[0]['AuthID'])+1);
		}
		
		if (data[0]['ParentJID'] !== null){
			getBreadcrumb(data[0]['ParentJID']);
		}
		
		
	}*/

	/*function postBreadcrumb(data){
		data = JSON.parse(data);
		
		//prepare to add a parent breadcrumb to breadcrum banner
		result = "<li class='breadcrumb-item' aria-current='" + data[0]['Name'] + "'>";
			result += 	"<button class='btn btn-sm btn-" + data[0]['CategoryColor'] + " breadcrumbButton' value='" + data[0]['JID'] + "'> " + data[0]['Name'] + " </button>";
		result += "</li>";
		
		//add the parent breadcrumb
		$('#jobBreadcrumbTrail').prepend(result);
		
		if (data[0]['ParentJID'] !== null){
			getBreadcrumb(data[0]['ParentJID']);
		}
	}*/
	
	//ADD BREADCRUMB BUTTON EVENT HANDLER
	/*$('#mainSection').on('click', '.breadcrumbButton', function(){
		openJob($(this).val());
	});*/


	//Event handler for "New Subtask" button
	/*$('#mainSection').on('click', '#createSubtask', function(){
		//console.log("VALUE: " + $('#JobID').val());
		var parentjid = $('#JobID').val()+'';
		var parentAuthLevel= parseInt($('#JobAuthID').val());
		var childAuthLevel= parentAuthLevel+1;
		$("#mainSection").load("view_newJob.txt", function() {
			$('#jobParent').val(parentjid),
			$('#jobAuthLevel').val(childAuthLevel)
		});
	});*/




	//turn a numerical priority into a string for display
	/*function priorityToString(priInt){
		switch (priInt){
				case '1':
					var priority = "Low";
					break;
				case '2':
					var priority = "Medium";
					break;
				case '3':
					var priority = "High";
					break;
				default:
					var priority = "None";
					break;
			}
		return priority;
	}*/


	/*function showEditJobDetails(data){
		data = JSON.parse(data);
		
		$('#jobID').val(data[0]['JID']);
		$('#jobDescription').val(data[0]['Description']);
		$('#jobName').val(data[0]['Name']);
		$('#jobStart').val(data[0]['StartDate']);
		$('#jobEnd').val(data[0]['EndDate']);
		$('#jobPriority').val(data[0]['Priority']);
		$('.JIDT').html(data[0]['AuthName']);
		$('#JobAuthID').val(data[0]['AuthID']);
		//$('#jobParent').val(data[0]['ParentJID']);
		$('#jobAuthLevel').val(data[0]['AuthID']);
		
		
		var request = {page: "Main", command: "GetJobStatusDetail"};
        var url = 'controller.php';
        $.post(url, request, function(StatData){
			StatData = JSON.parse(StatData);
			if(StatData){
				//create status options for dropdown
				for (var i = 0; i < StatData.length; i++){
					$('#jobStatus').append("<option value='" + StatData[i]['StatusID'] + "'>" + StatData[i]['Name'] + "</option>");
				}
				$('#jobStatus').val(data[0]['StatusID']);
				//console.log("Status ID: " + $('#jobStatus').val());
			}
		});
		
		request = {page: "Main", command: "GetJobCategoryDetail"};
        url = 'controller.php';
        $.post(url, request, function(CatData){
			CatData = JSON.parse(CatData);
			if(CatData){
				//create categories for dropdown
				for (var i = 0; i < CatData.length; i++){
					$('#jobCategory').append("<option value='" + CatData[i]['CategoryID'] + "' class='text-" + CatData[i]['Color'] + "'>" + CatData[i]['Name'] + "</option>");
				}
				$('#jobCategory').val(data[0]['CategoryID']);
				//console.log("Cat ID: " + $('#jobCategory').val());
			}
		});
		
	}*/


});
</script>

