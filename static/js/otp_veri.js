
function validateEmail() {
    const email = document.getElementById("email")
    console.log(email.value)
    load = document.getElementById("email_err")
    load.innerHTML = `<button class="btn" type="button" style="margin:10px">
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Verifying your email please wait...
  </button>`
    checkEmail(email.value)
}

async function checkEmail(email) {
    try {
        const response = await fetch("/auth/otp_verification/check_email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ "email": email }),
        });
        const result = await response.json();
        if (result.email) {
            email_in = document.getElementById("email")
            email = email_in.value;
            email_in.disabled = true;
            btn = document.getElementById("mail-btn")
            btn.remove();
            console.log("Success:", result);
            document.getElementById("email_err").innerHTML = ""
            otp_div = document.getElementById("otp_div")
            otp_div.innerHTML = `<div class="fw-normal text-muted mb-4" style="margin-top: 30px;">
            Enter OTP
        </div>
            <div class="otp-container">
            <input id="otp1" name="otp" type="number" class="form-control otp-input" maxlength="1" oninput="moveToNextInput(this, 2)" >
            <input id="otp2" type="number" class="form-control otp-input" maxlength="1" oninput="moveToNextInput(this, 3)" >
            <input id="otp3" type="number" class="form-control otp-input" maxlength="1" oninput="moveToNextInput(this, 4)" >
            <input id="otp4" type="number" class="form-control otp-input" maxlength="1" oninput="moveToNextInput(this, 5)" >
            <input id="otp5" type="number" class="form-control otp-input" maxlength="1" oninput="moveToNextInput(this, 6)" >
            <input id="otp6" type="number" class="form-control otp-input" maxlength="1" >
        </div>
        <div id="otp_err"></div>
        <button id="otp-btn" type="submit" onclick="verifyOTP()" class="btn btn-dark submit_btn my-4" style="width: 100%;">Submit</button>
        `
        }
        else {
            document.getElementById("email_err").innerHTML = "<p style='color:red;margin:10px'>Email not found<p>"
        }
        return result
    } catch (error) {
        console.error("Error:", error);
    }
}

 async function verifyOTP() {
    document.getElementById("otp_err").innerHTML = ""
    otp1 = document.getElementById("otp1").value;
    otp2 = document.getElementById("otp2").value;
    otp3 = document.getElementById("otp3").value;
    otp4 = document.getElementById("otp4").value;
    otp5 = document.getElementById("otp5").value;
    otp6 = document.getElementById("otp6").value;
    const otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6;
    console.log(otp)
    check = await verify_otp(otp);
    console.log("check",await check)
    if(check) {
        window.location.href= "/auth/reset_password"
    }
    else {
        document.getElementById("otp_err").innerHTML = `<p style='color:red;margin:10px'>Invalid OTP<p>`

    }
}

async function verify_otp(otp) {
    try {
        const response = await fetch("/auth/otp_verification/check_otp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "otp": otp
            }),
        });
        const result = await response.json();
        console.log(await result.isValid)
        return await result.isValid
    } catch (error) {
        console.error("Error:", error);
    }
}
