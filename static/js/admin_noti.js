async function replaceCardContent() {
  const announcementInput = document.getElementById('announcementInput');
  const subjectInput = document.getElementById('subjectInput');
  //console.log(subjectInput.value)
  const originalCard = document.querySelector('.notification');
  if (announcementInput.value == '' || announcementInput.value == ' ' || announcementInput.value == '  ' || announcementInput.value == '   ') {
    alert("Please enter notification")
    return false;
  }
  console.log(announcementInput.value)
  const response = await fetch("/admin/notifications/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "subject": subjectInput.value, "content": announcementInput.value }),
  });
  const result = await response.json();
  if (announcementInput.value.trim() !== '') {
    // Clear the input
    announcementInput.value = '';
    subjectInput.value = '';
    window.location = '/admin/notifications/'
  }
}

function showModal(noti, sub, time) {
  // Get the modal element
  var modal = document.getElementById("myModal");
  // Get the content element within the modal
  var modalContent = document.getElementById("modalContent");
  var modalFooter = document.getElementById("modalFooter");
  var modalTitle = document.querySelector('.modal-title')
  // Set the content within the modal
  modalTitle.innerHTML = '<b>' + sub + '</b>'
  modalContent.innerHTML = noti + '<br><br>';
  modalFooter.innerHTML = '<div class="text-end" style="font-size:15px">' + time + '</div>'
  // Display the modal
  var modalInstance = new bootstrap.Modal(modal);
  modalInstance.show();
}

function deleteNoti(id) {
  if (!window.confirm("Are you sure you want to delete the notification?")) {
    Event.preventDefault();
  }
  else{
    window.location.href="/admin/notifications/delete?id="+id;
  }
}
