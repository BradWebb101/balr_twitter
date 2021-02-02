// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var chart
function invokeChart() {
var ctx = document.getElementById("myPieChart");
chart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: dbData.lang_labels,
    datasets: [{
      data: dbData.lang_data,
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
      position: 'right'
    },
    cutoutPercentage: 60,
  },
})
}
