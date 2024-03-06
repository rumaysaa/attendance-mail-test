var userID = document.getElementById('userID')
var frs_status = document.getElementById('frs-status')
var btns = document.getElementById('frs-btns')
var video;
var startButton;
var stopButton;
var sendButton;
let mediaRecorder;
let recordedChunks = [];

function show_btns() {
  btns.innerHTML = `<div class="text-center">
  <a id="startButton" onclick="startRec()" class="btn btn-primary mt-1 mb-1">Start Recording</a>
  <a id="stopButton" onclick="stopRec()" class="btn btn-danger mt-1 mb-1">Stop Recording</a>
  <a id="sendButton" onclick="saveRec()" class="btn btn-secondary mt-1 mb-1">Submit Video</a>
  <div>
  <video id="video" width="640" height="480" autoplay></video>`
  video = document.getElementById('video');
  startButton = document.getElementById('startButton');
  stopButton = document.getElementById('stopButton');
  sendButton = document.getElementById('sendButton');
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    })
}

function startRec() {
  try {
    
    if (!mediaRecorder) {
      // If mediaRecorder is not initialized, request the camera stream
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          console.log("start")
          video.srcObject = stream;
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = handleDataAvailable;
          frs_status.innerHTML = ` <span style="color:red;margin-top:3px"><i class="bi bi-circle-fill"></i> &nbsp; Recording..</span>`
          mediaRecorder.start();
          fetch('/admin/users/save_userID', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "userid": userID.value }),
          })
        })
        .catch(error => {
          console.error('Error accessing media devices:', error);
        });
    } else {
      // If mediaRecorder is already initialized, just start it
      mediaRecorder.start();
      frs_status.innerHTML = ` <span style="color:red;margin-top:3px"><i class="bi bi-circle-fill"></i> &nbsp; Recording..</span>`;
    }
  } catch (error) {
    console.error('Error starting recording:', error);
  }
}


function stopRec() {
  try {
    // Stop the media recorder
    mediaRecorder.stop();

    // Stop the video track manually
    const srcObject = video.srcObject;
    if (srcObject) {
      video.srcObject = null;
      const tracks = srcObject.getTracks();
      tracks.forEach(track => {
        track.stop();
      });
    }

    // Clear status and log
    frs_status.innerHTML = '';
    console.log('Recording stopped successfully.');
  } catch (error) {
    console.error('Error stopping recording:', error);
  }
}

function clearMediaRecorderStream() {
  //if (mediaRecorder && mediaRecorder.stream) {
    // Stop the tracks in the stream
    mediaRecorder.stream.getTracks().forEach(track => {
      track.stop();
    });
    // Clear the stream from the media recorder
    mediaRecorder.stream = null;
  //}
  // Reset recordedChunks array and mediaRecorder object
  recordedChunks = [];
  mediaRecorder = null;
  console.log("Media stream cleared");
}
function saveRec() {
  console.log("send");
  frs_status.innerHTML = `<div class="text-center">
	<button class="btn" type="button" disabled>
	<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
	&nbsp; Processing face encodings...please wait..
  </button>
  </div>`
  const blob = new Blob(recordedChunks, { type: 'video/webm' });
  const formData = new FormData();
  formData.append('video', blob);

  fetch('/admin/users/save_video', {
    method: 'POST',
    body: formData
  }).then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    console.log('Video uploaded successfully');


    frs_status.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
        </symbol>
        <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
        </symbol>
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
        </symbol>
      </svg><div class="alert alert-success d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <div>
        Face Registered
        </div>
      </div>`
      clearMediaRecorderStream()

  })
    .catch(error => {
      console.error('Error uploading video:', error);
    });
};

function handleDataAvailable(event) {
  if (event.data.size > 0) {
    recordedChunks.push(event.data);
  }
}

async function save_face_enc() {

  console.log("hiiiiiii")
  console.log(userID.value)
  const response = await fetch("/admin/users/register_face_enc", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "userid": userID.value }),
  });

  const result = await response.json();
  if (result.status == true) {
    frs_status.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
        </symbol>
        <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
        </symbol>
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
        </symbol>
      </svg><div class="alert alert-success d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <div>
        Face Registered
        </div>
      </div>`
  }
  else if (result.status == false) {
    frs_status.innerHTML = `<div class="text-center">
        <div class="alert alert-danger" role="alert">
        Face not registered
        </div>
        </div>`
  }
}


$(document).ready(function () {
  // Function to fetch usernames from Flask server
  function fetchUsernames() {
    $.ajax({
      url: "/admin/users/getUsernames", // Update the URL to match your Flask route
      type: "GET",
      dataType: "json",
      success: function (data) {
        var userList = data.usernames;
        // Event listener for input change
        $("#username").on("input", function () {
          var typedUsername = $(this).val();

          // Check if typed username exists in the list
          if (userList.includes(typedUsername)) {
            // Username exists, disable submit button and show message
            $("#submitBtn").prop("disabled", true);
            $("#message").show(); // Show the message
            $(this).css("border-color", "red");
            $(this).css("color", "red");
          } else {
            // Username doesn't exist, enable submit button and hide message
            $("#submitBtn").prop("disabled", false);
            $("#message").hide(); // Hide the message
            $(this).css("border-color", ""); // Reset border color
            $(this).css("color", ""); // Reset text color
          }
        });
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error("Error fetching usernames:", textStatus, errorThrown);
      }
    });
  }

  // Call the function to fetch usernames when the document is ready
  fetchUsernames();
});
