function toggleDateFields() {
    var leaveType = document.getElementById("leaveType").value;
    var startDateLabel = document.getElementById("startDateLabel");
    var endDateGroup = document.getElementById("endDateGroup");
    var startHoursGroup = document.getElementById("startHoursGroup");
    var endHoursGroup = document.getElementById("endHoursGroup");

    if (leaveType === "Half day") {

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
    var reason = document.getElementById('reason').value;
    var startDate = document.getElementById("startDate").value;
    var endDate=null ;
    var startHours=null;
    var endHours=null;
    var empID = document.getElementById('empID').value;
    // Check if either start hours or end hours are empty, excluding hidden fields
    if (!isHidden(startHoursGroup) && !isHidden(endHoursGroup)) {
         startHours = document.getElementById("startHours").value;
         endHours = document.getElementById("endHours").value;

        if (!startHours || !endHours) {
            alert("Please fill in both start and end hours.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }
    }

    // Check if either start date or end date are empty, excluding hidden fields
    if (!isHidden(startDateGroup) && !isHidden(endDateGroup)) {
        endDate = document.getElementById("endDate").value;

        if (!startDate) {
            alert("Please fill in the start date.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }

        // Validate date format
        if (!validateDate(startDate)) {
            alert("Invalid date format. Please use dd-mm-yyyy.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }

        // Convert date strings to Date objects for comparison
        var startDateObj = new Date(startDate);
        var endDateObj = new Date(endDate);

        // Check if start date is in the future or today
        var today = new Date();
        today.setHours(0, 0, 0, 0); // Set time to midnight
        if (startDateObj < today) {
            alert("Start date must be today or in the future.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }
        if (!endDate) {
            alert("Please fill in the end date.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }
        // Check if start date is not more than end date
        if (startDateObj > endDateObj) {
            alert("Start date must be before or equal to end date.");
            event.preventDefault(); // Prevent further processing if validation fails
            return;
        }
    } else if ((leaveType === "Sick" || leaveType === "Casual") && !startDate) {
        alert("Please fill in both start and end dates for sick or personal leave.");
        event.preventDefault(); // Prevent further processing if validation fails
        return;
    } else if (!startDate) {
        alert("Please fill in the start date.");
        event.preventDefault;; // Prevent further processing if validation fails
        return;
    }
    if(!reason){
        alert("Please fill the reason")
        event.preventDefault();
        return;
    }
    
    var data={
        "empID":empID,
        "leaveType":leaveType,
        "startDate":startDate,
        "endDate":endDate,
        "startHr":startHours,
        "endHr":endHours,
        "reason":reason
    }
    const post =  postJSON(data)
    console.log(post)
    window.location.href = '/leave'
    
}

async function postJSON(data) {
	try {
		const response = await fetch("/leave/apply", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});
		const result = await response.json();
		console.log("Success:", result);
		return result
	} catch (error) {
		console.error("Error:", error);
	}
}