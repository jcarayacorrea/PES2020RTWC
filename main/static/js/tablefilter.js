function searchTable() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("tableTeams");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    // Skip header row if present
    if (tr[i].getElementsByTagName("th").length > 0) {
        continue;
    }
    
    let rowVisible = false;
    td = tr[i].getElementsByTagName("td");
    for (let j = 0; j < td.length; j++) {
      txtValue = td[j].textContent || td[j].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        rowVisible = true;
        break; 
      }
    }
    tr[i].style.display = rowVisible ? "" : "none";
  }
}