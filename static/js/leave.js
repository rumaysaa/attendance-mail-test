function toggleDateFields() {
    var leaveType = document.getElementById("leaveType").value;
    var startDateLabel = document.getElementById("startDateLabel");
    var endDateGroup = document.getElementById("endDateGroup");
    var startHoursGroup = document.getElementById("startHoursGroup");
    var endHoursGroup = document.getElementById("endHoursGroup");

    if (leaveType === "half day") {
        startDateLabel.textContent = "Start Date:";
        endDateGroup.classList.add("hidden");
        startHoursGroup.classList.remove("hidden");
        endHoursGroup.classList.remove("hidden");
    } else {
        startDateLabel.textContent = "Start Date:";
        endDateGroup.classList.remove("hidden");
        startHoursGroup.classList.add("hidden");
        endHoursGroup.classList.add("hidden");
    }
}
 

function openCalendar() {
    document.getElementById("startDate").focus();
}

function isHidden(element) {
    return element.classList.contains("hidden");
}

function validateDate(dateString) {
  // Validate date in yyyy-mm-dd format
  var dateRegex = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/;
  return dateRegex.test(dateString);
}

function submitLeaveRequest() {
  var leaveType = document.getElementById("leaveType").value;
  var startHoursGroup = document.getElementById("startHoursGroup");
  var endHoursGroup = document.getElementById("endHoursGroup");
  var startDateGroup = document.getElementById("startDateGroup");
  var endDateGroup = document.getElementById("endDateGroup");
    console.log(startHoursGroup,endHoursGroup)
  // Check if either start hours or end hours are empty, excluding hidden fields
  if (!isHidden(startHoursGroup) && !isHidden(endHoursGroup)) {
    var startHours = document.getElementById("startHours").value;
    var endHours = document.getElementById("endHours").value;

    if (!startHours || !endHours) {
      alert("Please fill in both start and end hours.");
      return; // Prevent further processing if validation fails
    }
  }

  // Check if either start date or end date are empty, excluding hidden fields
  if (!isHidden(startDateGroup) && !isHidden(endDateGroup)) {
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;

    if (!startDate) {
      alert("Please fill in the start date.");
      return; // Prevent further processing if validation fails
    }

    // Validate date format
    if (!validateDate(startDate)) {
      alert("Invalid date format. Please use dd-mm-yyyy.");
      return; // Prevent further processing if validation fails
    }

    // Convert date strings to Date objects for comparison
    var startDateObj = new Date(startDate);
    var endDateObj = new Date(endDate);

    // Check if start date is in the future or today
    var today = new Date();
    today.setHours(0, 0, 0, 0); // Set time to midnight
    if (startDateObj < today) {
      alert("Start date must be today or in the future.");
      return; // Prevent further processing if validation fails
    }

    // Check if start date is not more than end date
    if (startDateObj > endDateObj) {
      alert("Start date must be before or equal to end date.");
      return; // Prevent further processing if validation fails
    }
  } else if ((leaveType === "sick" || leaveType === "personal") && !startDate) {
    alert("Please fill in both start and end dates for sick or personal leave.");
    return; // Prevent further processing if validation fails
  } else if (!startDate) {
    alert("Please fill in the start date.");
    return; // Prevent further processing if validation fails
  }

  // Add your other form submission logic here
  // For example, you can submit the form using AJAX or perform other actions
  // ...

  // If everything is valid, you can proceed with the form submission
  alert("Leave request submitted successfully!");
}
    