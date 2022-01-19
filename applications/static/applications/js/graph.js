var school = document.querySelector("#id_school").value;
var schoolYear = document.getElementById("id_school_year").value;

var data =[];

for (const city of Object.keys(applicationCounts)) {
  data.push({
    x: ['Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10'],
    y: applicationCounts[city],
    name: city,
    type: 'bar'
  })
}

var layout = {
  xaxis: {title: 'Grade'},
  yaxis: {title: 'Number of Applications'},
  title: schoolYear+ ' '+school+' Application Report',
  barmode: 'stack'
 };

Plotly.newPlot('reportGraph', data, layout);
