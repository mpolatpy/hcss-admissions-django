var table = document.getElementById("applicationTable");
var dropdowns = document.getElementsByTagName("select");
var title = document.querySelector("h6");

for(let i = 0; i<dropdowns.length; i++){
  dropdowns[i].onchange = filter_table; 
}

// function filterTable() {
//   const filter = document.querySelector('#tableFilter').value.toUpperCase();
//   const trs = document.querySelectorAll('#applicationTable tr:not(.header)');
//   trs.forEach((tr => tr.style.display = [...tr.children].find(td => td.innerHTML.toUpperCase().includes(filter))) ? '' : 'none');
// }

var trs = document.querySelectorAll('#applicationTable tr:not(.header)');
var searchBox = document.querySelector('input');
searchBox.addEventListener('keyup', filter_table);

function filter_table(e){
  const selectSchoolYear = document.querySelector('#selectSchoolYear').value.toLowerCase();
  const selectSchool = document.querySelector('#selectSchool').value.toLowerCase();
  const selectGrade = document.querySelector('#selectGrade').value;
  const selectName = document.querySelector('#tableFilter').value.toLowerCase();

  title.style.display = 'none';
  table.style.display = '';

  trs.forEach(function(tr){
    let schoolYear = tr.children[0];
    let school = tr.children[1];
    let grade = tr.children[2];
    let first = tr.children[3];
    let last = tr.children[4];

    let schoolYearCondition = schoolYear.innerHTML.toLowerCase().includes(selectSchoolYear);
    let schoolCondition = school.innerHTML.toLowerCase().includes(selectSchool) || school.innerHTML.toLowerCase().includes('both');
    let gradeCondition = grade.innerHTML.includes(selectGrade);
    let nameCondition = first.innerHTML.toLowerCase().includes(selectName) || last.innerHTML.toLowerCase().includes(selectName);

    if(schoolYearCondition && schoolCondition && gradeCondition && nameCondition){
      tr.style.display = '';
    } else{
      tr.style.display = 'none';
    }
  });
}
