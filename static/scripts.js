var url_path = window.location.pathname

function filterIssueTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#issueTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          var thirdCol = rows[i].cells[2].textContent.toUpperCase();
          var fourthCol = rows[i].cells[3].textContent.toUpperCase();
          var sixthCol = rows[i].cells[5].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1 || fourthCol.indexOf(filter) > -1 || sixthCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

function filterAssetTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#assetTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          var thirdCol = rows[i].cells[2].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

function filterEngagementTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#engagementTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          var thirdCol = rows[i].cells[2].textContent.toUpperCase();
          var fourthCol = rows[i].cells[3].textContent.toUpperCase();
          var sixthCol = rows[i].cells[5].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1 || fourthCol.indexOf(filter) > -1 || sixthCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

function filterTestTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#testTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          var thirdCol = rows[i].cells[2].textContent.toUpperCase();
          var fourthCol = rows[i].cells[3].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1 || fourthCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

function filterTpTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#tpTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          var thirdCol = rows[i].cells[2].textContent.toUpperCase();
          var sixthCol = rows[i].cells[5].textContent.toUpperCase();
          var seventhCol = rows[i].cells[6].textContent.toUpperCase();
          var eigthCol = rows[i].cells[7].textContent.toUpperCase();
          var ninthCol = rows[i].cells[7].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1 || sixthCol.indexOf(filter) > -1 || seventhCol.indexOf(filter) > -1 || eigthCol.indexOf(filter) > -1 || ninthCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

function updateTable(event) {
      var filter = event.target.value.toUpperCase();
      var rows = document.querySelector("#updateTable tbody").rows;

      for (var i = 0; i < rows.length; i++) {
          var firstCol = rows[i].cells[0].textContent.toUpperCase();
          var secondCol = rows[i].cells[1].textContent.toUpperCase();
          if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1) {
              rows[i].style.display = "";
          } else {
              rows[i].style.display = "none";
          }
      }
  }

if (url_path == "/submitisa") {

    document.getElementById('new_application').addEventListener('change', function () {
      if(this.value == "No") {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('new_app_label').style.display = style;
        document.getElementById('new_application_name').style.display = style;
      }
      if(this.value == "Yes") {
        var style = this.value == 1 ? 'block' : 'inherit';
        document.getElementById('new_app_label').style.display = style;
        document.getElementById('new_application_name').style.display = style;
      }
    })

    document.getElementById('existing_application').addEventListener('change', function () {
      if(this.value == "No") {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('existing_application_label').style.display = style;
        document.getElementById('existing_application_name').style.display = style;
        document.getElementById('existing_application_changes').style.display = style;
        document.getElementById('existing_changes_label').style.display = style;
      }
      if(this.value == "Yes") {
        var style = this.value == 1 ? 'block' : 'inherit';
        document.getElementById('existing_application_label').style.display = style;
        document.getElementById('existing_application_name').style.display = style;
        document.getElementById('existing_application_changes').style.display = style;
        document.getElementById('existing_changes_label').style.display = style;
      }
    })

    document.getElementById('third_party_involvement').addEventListener('change', function () {
      if(this.value == "No") {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('third_party_name_label').style.display = style;
        document.getElementById('third_party_name').style.display = style;
        document.getElementById('third_party_service_label').style.display = style;
        document.getElementById('third_party_services').style.display = style;
      }
      if(this.value == "Yes") {
        var style = this.value == 1 ? 'block' : 'inherit';
        document.getElementById('third_party_name_label').style.display = style;
        document.getElementById('third_party_name').style.display = style;
        document.getElementById('third_party_service_label').style.display = style;
        document.getElementById('third_party_services').style.display = style;
      }
    })

    document.getElementById('project_name_label').addEventListener('mouseover', function () {
      {
        var style = this.value == 1 ? 'block' : 'inline-block';
        document.getElementById('tool_tip_project_name').style.display = style;
      }
    })
    document.getElementById('project_name_label').addEventListener('mouseout', function () {
      {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('tool_tip_project_name').style.display = style;
      }
    })

    document.getElementById('main_contact_label').addEventListener('mouseover', function () {
      {
        var style = this.value == 1 ? 'block' : 'inline-block';
        document.getElementById('tool_tip_main_contact').style.display = style;
      }
    })
    document.getElementById('main_contact_label').addEventListener('mouseout', function () {
      {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('tool_tip_main_contact').style.display = style;
      }
    })

    document.getElementById('description_label').addEventListener('mouseover', function () {
      {
        var style = this.value == 1 ? 'block' : 'inline-block';
        document.getElementById('tool_tip_description').style.display = style;
      }
    })
    document.getElementById('description_label').addEventListener('mouseout', function () {
      {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('tool_tip_description').style.display = style;
      }
    })

    document.getElementById('new_application_label').addEventListener('mouseover', function () {
      {
        var style = this.value == 1 ? 'block' : 'inline-block';
        document.getElementById('tool_tip_new_app_house').style.display = style;
      }
    })
    document.getElementById('new_application_label').addEventListener('mouseout', function () {
      {
        var style = this.value == 1 ? 'block' : 'none';
        document.getElementById('tool_tip_new_app_house').style.display = style;
      }
    })
}

if (url_path == "/viewassets") {
  document.querySelector('#assetFilterInput').addEventListener('keyup', filterAssetTable, false);
}
if (url_path == "/viewissues") {
  document.querySelector('#issueFilterInput').addEventListener('keyup', filterIssueTable, false);
}
if (url_path == "/viewengagements") {
  document.querySelector('#engagementFilterInput').addEventListener('keyup', filterEngagementTable, false);
}
if (url_path == "/viewtests") {
  document.querySelector('#testFilterInput').addEventListener('keyup', filterTestTable, false);
}
if (url_path == "/viewthirdparty") {
  document.querySelector('#tpFilterInput').addEventListener('keyup', filterTpTable, false);
}
if (url_path.indexOf("update") !== -1) {
  document.querySelector('#updateFilterInput').addEventListener('keyup', updateTable, false);
}
if (url_path.indexOf("create") !== -1) {
  document.querySelector('#updateFilterInput').addEventListener('keyup', updateTable, false);
}
if (url_path == "/engagements") {
  document.querySelector('#updateFilterInput').addEventListener('keyup', updateTable, false);
}
if (url_path == "/openengagements") {
  document.querySelector('#engagementFilterInput').addEventListener('keyup', filterEngagementTable, false);
}
