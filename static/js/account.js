async function change_pwd() {
    try {
        const old_pwd = document.getElementById("old_pwd");
        const new_pwd = document.getElementById("new_pwd1");
        const conf_new_pwd = document.getElementById("new_pwd2");
        if(old_pwd.value == '' || new_pwd.value == '' || conf_new_pwd.value == ''){
            return alert("Enter valid value")
        }
        const empID = document.getElementById("emp_id");
        const data = { "empID": empID.value ,"old_pwd": old_pwd.value, "new_pwd1": new_pwd.value, "new_pwd2": conf_new_pwd.value }
        const response = await fetch("/account/update_pwd", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if(result.oldpwd_err != null){
            const olddiv = document.getElementById("old_pwd_err")
            olddiv.innerHTML = "<p style='color: red;'>Incorrect password</p>"
        }
        if(result.unmatched_err != null){
            const unmatchdiv = document.getElementById("not_match_err")
            unmatchdiv.innerHTML = "<p style='color: red;'>Password not matched</p>"
        }
        if(result.change_success != null){
            document.location.href = "/account/redirect_loader";
        }
        console.log(result)
        return result
    } catch (error) {
        console.error("Error:", error);
    }
}

function onAvatarClick(){
    const avatar = document.getElementById("avatar-div")
    const form_con = document.getElementById("form-container")
    const btn = document.getElementById('avatar-btn')
    if(avatar.style.display == "block"){
        avatar.style.display = "none";
        form_con.style.display = "block" 
        btn.innerHTML = `<span style="color: grey; font-size: 12px;"><i class='bx bx-edit'></i>
        <span>Change Avatar</span></span>`
    }
    else if(avatar.style.display == "none"){
        avatar.style.display = "block";
        form_con.style.display = "none"
        btn.innerHTML =   `<span style="color: grey; font-size: 12px;">
        <span>Show Profile</span></span>`
    }
    const prev = document.querySelector('.left')
    const next = document.querySelector('.right')
    const container = document.querySelector('.avatars')
    const avatars = document.querySelectorAll('.avatars-container .avatar-item')
    let currentIndex = Math.floor(avatars.length/2)
    const val = (avatars.length - 1 - Math.floor(avatars.length/2)) * 195
    let translateVal = 0
  
    for (let i = 0; i < avatars.length; i++) {
      if (i === Math.floor(avatars.length/2)) {
        avatars[i].classList.add('current')
      }
      avatars[i].addEventListener('click', () => {
        console.log(document.getElementsByName('avatar'))
      })
    }
  
    let defaultVal = 0
    if (avatars.length % 2 === 0) {
      defaultVal = 90
      translateVal -= 90
      container.style.transform = `translateX(${translateVal}px)`
    }
  
  
    prev.addEventListener('click', () => {
      if (currentIndex - 1 < 0) {
        avatars[currentIndex].classList.remove('current')
        avatars[avatars.length - 1].classList.add('current')
        currentIndex = avatars.length - 1
        translateVal = -val - defaultVal
        container.style.transform = `translateX(${translateVal}px)`
      } else {
        avatars[currentIndex].classList.remove('current')
        avatars[currentIndex - 1].classList.add('current')
        currentIndex -= 1
        translateVal += 195
        container.style.transform = `translateX(${translateVal}px)`
      }
    })
  
    next.addEventListener('click', () => {
      if (currentIndex + 1 >= avatars.length) {
        avatars[currentIndex].classList.remove('current')
        avatars[0].classList.add('current')
        currentIndex = 0
        translateVal = val + defaultVal
        container.style.transform = `translateX(${translateVal}px)`
        return
      }
      avatars[currentIndex].classList.remove('current')
      avatars[currentIndex + 1].classList.add('current')
      currentIndex += 1
      translateVal -= 195
      container.style.transform = `translateX(${translateVal}px)`
    })
  
  }

  function showWeek(){
    const weeks = document.getElementById('weekdays')
    console.log(weeks.style.display == "inline-block")
    if(weeks.style.display == "inline-block"){
      weeks.style.display = "none"
    }
    else if(weeks.style.display == "none"){
    weeks.style.display = "inline-block"
  }
  }
  function submitDays(){
    const list = new Array();
    vals = document.getElementsByName('days')
    for(let i=0; i<vals.length;i++){
      if(vals[i].checked==true){
      list.push(vals[i].value)
      }
    }
    emp_id = document.getElementById('emp_id').value
    console.log(list)
    postJSON(emp_id,list)
    window.location.href = '/account/'
  }

  async function postJSON(id,weekdays) {
    try {
      const response = await fetch("/account/set_reminder", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ "id": id, "days":weekdays }),
      });
  
      const result = await response.json();
      console.log("Success:", result);
      return result
    } catch (error) {
      console.error("Error:", error);
    }
  }