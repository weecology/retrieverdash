function searchFunction() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("datasetTable");
    checkFailOnly = document.getElementById("fail-only");
    tr = table.getElementsByTagName("tr");

    failOnlyState = checkFailOnly.checked;
    if (failOnlyState) {
        for (i = 0; i < tr.length; i++) {
            if (i == 0) {
                continue;
            }
            failState = tr[i].getElementsByTagName("td")[1].innerHTML == "Failing";
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                if (failState && td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    } else {
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}