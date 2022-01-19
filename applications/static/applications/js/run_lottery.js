var model = {
  currentList: [],
  applications: application_list
};

var controller = {
  init: function(){
    lotteryView.init();
    this.selectSchoolYear = document.getElementById('lotterySchoolYear');
    this.selectSchool = document.getElementById('lotterySchool');
    this.selectGrade = document.getElementById('lotteryGrade');
  },

  getCurrentList: function(){
    return model.currentList;
  },

  getApplications: function(){
    return model.applications;
  },

  setCurrentList: function(){
    const selectSchoolYear = this.selectSchoolYear.value;
    const selectSchool = document.getElementById('lotterySchool').value.toLowerCase();
    const selectGrade = document.getElementById('lotteryGrade').value;
    model.currentList = model.applications.filter( function(applicant) {
      return (applicant.application__school_year === selectSchoolYear && applicant.application__grade === selectGrade && (applicant.application__school.toLowerCase().includes(selectSchool) || applicant.application__school.toLowerCase() === 'both schools' ))
    });
    assignLotteryPreference(model.currentList, selectSchool);
  },

  runLottery: function(){
    let currentList = this.getCurrentList();
    currentList.forEach((student) => {
      student.randomNumber = Math.random();
    });
    lotteryView.li_run_lottery.style.display = 'none';
    lotteryView.li_sort_lottery.style.display = '';
  },

  sortCurrentList: function(){
    const currentList = this.getCurrentList();

    currentList.sort( function(a, b){
      const status_map = {
        'Sibling': 1,
        'Resident': 2,
        'Non-Resident': 3
      };
      if ( a.status === b.status){
        return a.randomNumber - b.randomNumber;
      } else {
        return status_map[a.status] - status_map[b.status];
      }
    });

    currentList.forEach((item, i) => {
      item.order = i + 1;
    });
  },

  postLotteryData: function(){
    const input = document.getElementById('id_lotterydata');
    const data = this.getCurrentList();
    input.value = JSON.stringify(data);
  }

};

var lotteryView = {
  init: function(){
    this.lotteryFilterButton = document.querySelector('#lotteryFilterButton');
    this.tableBody = document.querySelector('#lotteryTableBody');
    this.lotteryRunButton = document.querySelector('#lotteryRunButton');
    this.li_lottery_list = document.querySelector('#li_lottery_list');
    this.lotterySortButton = document.querySelector('#lotterySortButton');
    this.li_run_lottery = document.querySelector('#li_run_lottery');
    this.li_sort_lottery = document.querySelector('#li_sort_lottery');
    this.li_save_lottery = document.querySelector('#li_save_lottery');
    this.lotteryData = document.getElementById('id_lotterydata');

    this.lotteryFilterButton.addEventListener('click', () => {
        controller.setCurrentList();
        this.li_lottery_list.style.display = 'none';
        this.li_run_lottery.style.display = '';
        this.render();
    });

    this.lotteryRunButton.addEventListener('click', () => {
      controller.runLottery();
      this.render();
    });

    this.lotterySortButton.addEventListener('click', () => {
      controller.sortCurrentList();
      this.li_sort_lottery.style.display = 'none';
      this.li_save_lottery.style.display = '';
      this.render();
      controller.postLotteryData();
    });

  },

  render: function(){
    let currentList = controller.getCurrentList();
    let tableBody = this.tableBody;
    tableBody.innerHTML = '';

    currentList.forEach(function(applicant){
      let tr = createTableRow(applicant);
      tableBody.appendChild(tr);
    })
  }
};

function createTableRow(student){
      let tr = document.createElement('tr');
      let applicationId = document.createElement('td');
      applicationId.textContent = student.id;
      let name = document.createElement('td');
      name.textContent = (student.first_name.substring(0,1) + student.last_name.substring(0,1)).toUpperCase();
      let randomNumber = document.createElement('td');
      randomNumber.textContent = student.randomNumber? student.randomNumber : '';
      let order = document.createElement('td');
      order.textContent = student.order? student.order : '';
      let status = document.createElement('td');
      status.textContent = student.status? student.status : '';
      let city = document.createElement('td');
      city.textContent = student.address__city;
      tr.appendChild(order);
      tr.appendChild(randomNumber);
      tr.appendChild(applicationId);
      tr.appendChild(name);
      tr.appendChild(city);
      tr.appendChild(status);

      return tr;
}

function assignLotteryPreference(applicationList, school){
  const towns = {
    'hcss east': ['chicopee', 'ludlow', 'springfield', 'west springfield'],
    'hcss west': ['west springfield', 'holyoke', 'westfield', 'agawam']
  };

  const townList = towns[school.toLowerCase()];

  applicationList.forEach((student) => {
    if (student.has_sibling){
      student.status = 'Sibling';
    } else if ( townList.includes(student.address__city.toLowerCase()) ) {
      student.status = 'Resident';
    } else {
      student.status = 'Non-Resident';
    }
  });

}

controller.init();

// var tableBody = document.getElementsByTagName('tbody')[0];
// var lotteryFilterButton = document.querySelector('#lotteryFilterButton');
// var filtered_list = [];
//
// lotteryFilterButton.addEventListener('click', function(e){
//   const selectSchoolYear = document.getElementById('lotterySchoolYear').value;
//   const selectSchool = document.getElementById('lotterySchool').value.toLowerCase();
//   const selectGrade = document.getElementById('lotteryGrade').value;
//   filtered_list= application_list.filter( function(applicant) {
//     return (applicant.school_year === selectSchoolYear && applicant.grade === selectGrade && (applicant.school.toLowerCase().includes(selectSchool) || applicant.school.toLowerCase() === 'both schools' ))
//   });
//   tableBody.innerHTML = '';
//   for (let student of filtered_list){
//     let tr = document.createElement('tr');
//     let applicationId = document.createElement('td');
//     applicationId.textContent = student.applicant__pk;
//     let name = document.createElement('td');
//     name.textContent = (student.applicant__first_name.substring(0,1) + student.applicant__last_name.substring(0,1)).toUpperCase();
//     let randomNumber = document.createElement('td');
//     randomNumber.textContent = '';
//     let order = document.createElement('td');
//     order.textContent = '';
//     let status = document.createElement('td');
//     status.textContent = '';
//     tr.appendChild(order);
//     tr.appendChild(applicationId);
//     tr.appendChild(name);
//     tr.appendChild(randomNumber);
//     tr.appendChild(status);
//     tableBody.appendChild(tr);
//     console.log('item added');
//   }
// });
// const trs = document.querySelectorAll('#lotteryTable tr:not(.header)');
// const table = document.querySelector('#lotteryTable');
// const lotteryTitle = document.querySelector('#lotteryTitle');
// const dropdowns = document.getElementsByTagName('select');
// console.log(allApplications);
//
// for (let i=0; i < dropdowns.length; i++){
//   dropdowns[i].onchange = filter_lottery;
// }
//
// function filter_lottery(e){
//   const selectSchoolYear = document.querySelector('#lotterySchoolYear').value.toLowerCase();
//   const selectSchool = document.querySelector('#lotterySchool').value.toLowerCase();
//   const selectGrade = document.querySelector('#lotteryGrade').value;
//
//   lotteryTitle.style.display = 'none';
//   table.style.display = '';
//
//   trs.forEach(function(tr){
//     let schoolYear = tr.children[0];
//     let school = tr.children[1];
//     let grade = tr.children[2];
//     let schoolYearCondition = schoolYear.innerHTML.toLowerCase().includes(selectSchoolYear);
//     let schoolCondition = school.innerHTML.toLowerCase().includes(selectSchool) || school.innerHTML.toLowerCase().includes('both');
//     let gradeCondition = grade.innerHTML.includes(selectGrade);
//
//     if(schoolYearCondition && schoolCondition && gradeCondition){
//       tr.style.display = '';
//     } else{
//       tr.style.display = 'none';
//     }
//   });
// }
