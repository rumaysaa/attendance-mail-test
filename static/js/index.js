/*document.addEventListener("DOMContentLoaded", function (event) {

  const linkColor = document.querySelectorAll('.nav_link')

  function colorLink() {
      if (linkColor) {
          linkColor.forEach(l => l.classList.remove('active'))
          this.classList.add('active')
      }
  }
  linkColor.forEach(l => l.addEventListener('click', colorLink))

  // Your code to run since DOM is loaded and ready
}); */

$(document).ready(function() {
  clockUpdate();
  setInterval(clockUpdate, 1000);

 
  $(document).on('click', function (e) {
    var navbar = $('.l-navbar');
   
    // If the clicked element is not a descendant of the l-navbar and not the sidebartoggler, remove the show class
    if (!navbar.is(e.target) && navbar.has(e.target).length === 0 && !$("#sidebartoggler").is(e.target)) {
        navbar.removeClass('show');
    }
});

// Toggle the show class when the sidebartoggler is clicked
$("#sidebartoggler").click(function (e) {
    e.stopPropagation(); // Prevent the click event from reaching the document
    $(".l-navbar").toggleClass("show");
});

  console.log("helo")
})



function clockUpdate() {
  var date = new Date();
  $('.digital-clock').css({'color': '#000'});
  function addZero(x) {
    if (x < 10) {
      return x = '0' + x;
    } else {
      return x;
    }
  }

  function twelveHour(x) {
    if (x > 12) {
      return x = x - 12;
    } else if (x == 0) {
      return x = 12;
    } else {
      return x;
    }
  }

  var h = addZero(twelveHour(date.getHours()));
  var m = addZero(date.getMinutes());
  var s = addZero(date.getSeconds());

  $('.digital-clock').text(h + ':' + m + ':' + s)
}