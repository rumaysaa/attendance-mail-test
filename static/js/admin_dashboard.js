const charts = document.querySelectorAll(".chart");

charts.forEach(async function (chart) {
  var ctx = chart.getContext("2d");
  const url = '/admin/cal_working_hour'
  const response = await (await fetch(url)).json()
  let i;
  var names = new Array();
  var w_hrs = new Array();
  var b_hrs = new Array();
  for(i=0;i<response.length;i++){
    names.push(response[i].name)
    w_hrs.push(response[i].working_hrs)
    b_hrs.push(response[i].break_hrs)
  }
  console.log(response)
  if(response.length==0){
    var display = document.getElementById('display')
    console.log(display)
    display.innerHTML = 'No data'
  }
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: names,
      datasets: [
        {
          label: "Working hours",
          data: w_hrs,
          stack: 'Stack 0',
          backgroundColor: [
            
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(80, 100, 200, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(80, 100, 200, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
        { 
          label: 'Break hours', 
          backgroundColor: "rgba(255, 99, 132, 0.2)", 
          borderColor: "rgba(255, 99, 132, 1)",
          data: b_hrs, 
          stack: 'Stack 0', 
          borderWidth: 1
      }
      ],
    },
    options: {
      plugins: {
        legend: {
           display: false
        }
     },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});




$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable();
  });
 
});

