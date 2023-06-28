
//highlight rows on mouseover
function highlightRow(row) {
    row.classList.add("highlighted-row");
}

function unhighlightRow(row) {
    row.classList.remove("highlighted-row");
}


//sort table by row when header is clicked
function sortTable(columnIndex) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  
  table = document.getElementById("player_table");


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