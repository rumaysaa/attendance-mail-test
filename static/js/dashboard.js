var checkinbtn = document.getElementById("checkInBtn");
var checkoutbtn = document.getElementById("checkOutBtn");
var table = document.getElementById("myAtt");
var include_div = document.getElementById("inner_page_load")
hrs = document.getElementById("hrs")
var modal_submit = document.getElementById("modalBtn")
var task_type = document.getElementsByName("task_type")
var desc = document.getElementById("tasks")
var loader = document.getElementById('frs-loader')
var out_loader = document.getElementById('checkout-frs-loader')
var projID = document.getElementById('projectID')
var frs_status = document.getElementById('frs-status')
const video = document.getElementById('video');
var task_type_value, projid, status_ = null;
previous_hrs = 0
var MatchFound;
var proj_flag = 0

//var nav_link = document.getElementById("dash");
//nav_link.classList.add("active")

let mediaRecorder;
let recordedChunks = [];


$(document).ready(function () {
	if (checkinbtn.hidden == true) {
		workingClockUpdate();
		setTimeout(function () {
			workingClockUpdate
		}, 1000);
	}

})

async function workingClockUpdate() {
	const url = '/working_hr_count'
	const response = await (await fetch(url)).json()
	const hr = parseInt(response.hr[0])
	const min = parseInt(response.hr[1])
	const sec = parseInt(response.hr[2])
	$('#workinghrs').stopwatch({ startTime: ((hr * 60 * 60 * 1000) + (min * 60 * 1000) + (sec * 1000)) }).stopwatch('start');
};

async function startRec(stream, check) {
	video.srcObject = stream;
	mediaRecorder = new MediaRecorder(stream);
	mediaRecorder.ondataavailable = handleDataAvailable;
	mediaRecorder.start();
	return new Promise((resolve, reject) => {
		mediaRecorder.onstop = () => {
			const blob = new Blob(recordedChunks, { type: 'video/webm' });
			const formData = new FormData();
			formData.append('video', blob);
			fetch('/frs', {
				method: 'POST',
				body: formData
			}).then(async response => {
				status_ = (await response.json()).status_;
				console.log(status_)
				//status.ok
				if (status_ == "True") {
					if (check == "in") {
						let checkin = check_in()
						console.log("check_in", checkin)
					}
					else if (check == "out") {
						let checkout = await check_out()
						console.log("check_out", checkout)
					}
				}
				else if (!response.ok) {
					response.okreject(new Error('Network response was not ok'));

				}
				else if (status_ == "False") {
					loader.innerHTML = `<div class="text-center">
	<div class="alert alert-danger" role="alert">
 	Face not Recognised!
	</div>
	</div>`
				}
				resolve(response);
			}).catch(error => {
				reject(error);
			});
		};
	});
}
function getLocation() {
	return new Promise((resolve, reject) => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				function (position) {
					var latitude = position.coords.latitude.toFixed(5);
					var longitude = position.coords.longitude.toFixed(5);
					// Check if the first 5 digits of latitude and longitude match the specified values
					var matchFound = latitude.startsWith("21.142") && longitude.startsWith("72.7");
					resolve(matchFound);
				},
				function (error) {
					reject(error);
					loader.innerHTML = ''
					alert("Please allow location access");
					Event.preventDefault
				}
			);
		} else {
			alert("Please allow location access");
			reject("Location access not available");
		}
	});
}



function check_in() {
	setTimeout(function () {
		workingClockUpdate
	}, 1000);
	const url = '/checkin'
	getLocation().then(matchFound => {
		loader.innerHTML = ''
		timer = true;
		//stopWatch();
		workingClockUpdate();
		console.log("Match found:", matchFound);
		fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ "inoffice": matchFound })
		})
			.then(response => response.json())
			.then(json => {
				checkinbtn.hidden = true;
				checkoutbtn.hidden = false;
				document.getElementById("record_id").value = json.id
				var row = table.insertRow(1);
				var ip_html, checkin_status;
				if (json.in_ip_range) {
					ip_html = `<i class="bi bi-wifi"></i>`
				}
				else if (!json.in_ip_range) {
					ip_html = `<i class="bi bi-house-door"></i>`
				}
				else {
					ip_html = `<i class="bi bi-exclamation-triangle"></i>`
				}
				row.insertCell(0).innerHTML = ip_html;
				//row.insertCell(1).innerHTML = json.name;
				if (json.is_first_checkin) {
					if (json.in <= '09:30:00') {
						row.insertCell(1).innerHTML = json.in + `<span class="badge rounded-pill bg-success"
				style="margin: 3px;">Early</span>`;
					}
					if (json.in > '09:30:00') {
						row.insertCell(1).innerHTML = json.in + `<span class="badge rounded-pill bg-danger" style="margin: 3px;">Late</span>`
					}
				}
				else {
					row.insertCell(1).innerHTML = json.in;
				}
				row.insertCell(2).innerHTML = json.breakTime
				row.insertCell(3).innerHTML = ""
				row.insertCell(4).innerHTML = ""
			})
	}).catch(error => {
		console.error("Error occurred:", error);
	});
	return true
}

function endRec() {
	if (mediaRecorder && mediaRecorder.state !== 'inactive') {
		mediaRecorder.stop();
		const tracks = video.srcObject.getTracks();
		tracks.forEach(track => track.stop());
		video.srcObject = null;
	}
}
async function check_frs(check) {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({ video: true });
		console.log("Recording started...");
		setTimeout(() => {
			endRec(); // Call endRec function after 5 seconds
		}, 1000);
		await startRec(stream, check);
		console.log("Recording finished.");
		// Do other stuff after recording finishes
	} catch (error) {
		console.error("Error:", error);
		loader.innerHTML = `<div class="text-center">
            <div class="alert alert-danger" role="alert">
                Face not Recognised!
            </div>
        </div>`;
		//refresh()
	}
}
checkinbtn.addEventListener('click', async function () {
	clearMediaRecorderStream()
	loader.innerHTML = `<div class="text-center">
        <button class="btn" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            &nbsp; Recognizing your face..please wait..
        </button>
    </div>`;
	check_frs("in")
});

function clearMediaRecorderStream() {
	stream = null;
	recordedChunks = []
	mediaRecorder = null;;
	console.log("clearing")
	if (mediaRecorder && mediaRecorder.stream) {
		// Stop the tracks in the stream
		mediaRecorder.stream.getTracks().forEach(track => {
			track.stop();
		});
		// Clear the stream from the media recorder
		mediaRecorder.stream = null;
		console.log(mediaRecorder.stream)
	}
}

modal_submit.addEventListener('click', async function () {
	clearMediaRecorderStream()
	var i, flag = 0;
	for (i = 0; i < projID.length; i++) {
		if (projID[i].selected == true) {
			projid = projID[i].value
			proj_flag = 1
		}
	}
	if (proj_flag == 0) {
		alert("No project available")
		Event.preventDefault;
		return;
	}
	if (desc.value == '') {
		alert("Enter task description");
		Event.preventDefault;
		return;
	}
	for (i = 0; i < task_type.length; i++) {
		if (task_type[i].checked == true) {
			flag = 1;
			task_type_value = task_type[i].value
		}
	}
	if (flag == 0) {
		alert("Select task type");
		Event.preventDefault;
		return;
	}
	loader = document.getElementById('checkout-frs-loader')
	loader.innerHTML = `<div class="text-center">
	<button class="btn" type="button" disabled>
	<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
	&nbsp; Recognizing your face..please wait..
  </button>
  </div>`
	check_frs("out")
});

async function check_out() {
	var recID = document.getElementById("record_id").value
	var json = await postJSON(recID)
	table.deleteRow(1);
	var row = table.insertRow(1);
	if (json.in_ip_range) {
		ip_html = `<i class="bi bi-wifi"></i>`
	}
	else if (!json.in_ip_range) {
		ip_html = `<i class="bi bi-house-door"></i>`
	}
	else {
		ip_html = `<i class="bi bi-exclamation-triangle"></i>`
	}
	//row.insertCell(0).innerHTML = json.email;
	//row.insertCell(1).innerHTML = json.name;
	row.insertCell(0).innerHTML = ip_html;
	row.insertCell(1).innerHTML = json.in;
	row.insertCell(2).innerHTML = json.breakTime
	row.insertCell(3).innerHTML = json.out
	row.insertCell(4).innerHTML = json.totalhr
	tasks = (await fetch('/task_report', {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			"task_type": task_type_value,
			"projectID": projid,
			"desc": desc.value
		})
	}))
	loader.innerHTML = ''
	checkinbtn.hidden = false;
	checkoutbtn.hidden = true;
	refresh();
	return true
}

async function postJSON(data) {
	try {
		const response = await fetch("/checkout", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ "id": data }),
		});

		const result = await response.json();
		console.log("Success:", result);
		document.getElementById("record_id").value = null
		return result
	} catch (error) {
		console.error("Error:", error);
	}
}

function refresh() {
	window.location.href = "/"
}

let hour = 0;
let minute = 0;
let second = 0;
let count = 0;
function stopWatch() {
	if (timer) {
		count++;

		if (count == 100) {
			second++;
			count = 0;
		}

		if (second == 60) {
			minute++;
			second = 0;
		}

		if (minute == 60) {
			hour++;
			minute = 0;
			second = 0;
		}

		let hrString = hour;
		let minString = minute;
		let secString = second;
		let countString = count;

		if (hour < 10) {
			hrString = "0" + hrString;
		}

		if (minute < 10) {
			minString = "0" + minString;
		}

		if (second < 10) {
			secString = "0" + secString;
		}

		if (count < 10) {
			countString = "0" + countString;
		}

		document.getElementById('hr').innerHTML = hrString;
		document.getElementById('min').innerHTML = minString;
		document.getElementById('sec').innerHTML = secString;
		document.getElementById('count').innerHTML = countString;
		setTimeout(stopWatch, 10);
	}
}


function reset_time() {
	timer = false;
	hour = 0;
	minute = 0;
	second = 0;
	count = 0;
	document.getElementById('hr').innerHTML = "00";
	document.getElementById('min').innerHTML = "00";
	document.getElementById('sec').innerHTML = "00";
	document.getElementById('count').innerHTML = "00";
};
function handleDataAvailable(event) {
	if (event.data.size > 0) {
		recordedChunks.push(event.data);
	}
}


/// GEOLOCATION

function showError(error) {
	// Handle errors here
	console.log("Error occurred while getting location:", error);
}
