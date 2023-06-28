function highlightRow(row) {
    row.classList.add("highlighted-row");
}

function unhighlightRow(row) {
    row.classList.remove("highlighted-row");
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("defaultOpen").click();
});


function openCity(evt, cityName) {

  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

function sortTable(columnIndex, tabVal) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  if (tabVal == 0){
      table = document.getElementById("stat_table");
  }
  else{
      table = document.getElementById("odds_table");
  }
  switching = true;
  dir = "asc";

  while (switching) {
    switching = false;
    rows = table.getElementsByTagName("tr");

    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("td")[columnIndex];
      y = rows[i + 1].getElementsByTagName("td")[columnIndex];

      if (columnIndex === 0) {
        xValue = x.innerHTML.toLowerCase();
        yValue = y.innerHTML.toLowerCase();
      } else {
        xValue = parseFloat(x.innerHTML.replace(/[^0-9.-]+/g, ''));
        yValue = parseFloat(y.innerHTML.replace(/[^0-9.-]+/g, ''));
      }

      if (dir === "asc") {
        if (xValue > yValue) {
          shouldSwitch = true;
          break;
        }
      } else {
        if (xValue < yValue) {
          shouldSwitch = true;
          break;
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount++;
    } else {
      if (switchcount === 0 && dir === "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}