// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example

function getPieChart (lang_data){
var ctx = document.getElementById("myPieChart");
var chart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: lang_data['language_count_dict']['M']['labels']['L'].map(dict => dict['S']),
    datasets: [{
      data: lang_data['language_count_dict']['M']['data']['L'].map(dict => parseInt(dict['N'])),
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc','#f6c23e','#e74a3b'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#2c9faf','#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: true,
      position: 'bottom'
    },
    cutoutPercentage: 60,
  },
})
return chart};
