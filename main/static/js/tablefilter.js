/**
 * Search and filter a table by a search input
 */
const searchTable = () => {
    const input = document.getElementById("searchInput");
    const table = document.getElementById("tableTeams");
    if (!input || !table) return;

    const filter = input.value.toUpperCase();
    const rows = table.querySelectorAll("tbody tr:not(.no-results-row)");

    let visibleCount = 0;
    rows.forEach(row => {
        // Skip rows that contain header cells
        if (row.querySelector("th")) return;

        const cells = Array.from(row.querySelectorAll("td"));
        const matches = cells.some(td => 
            td.textContent.toUpperCase().includes(filter)
        );

        row.style.display = matches ? "" : "none";
        if (matches) visibleCount++;
    });

    // Handle "No results" message
    let noResultsRow = table.querySelector(".no-results-row");
    if (visibleCount === 0 && filter !== "") {
        if (!noResultsRow) {
            const tbody = table.querySelector("tbody");
            const colCount = table.querySelectorAll("thead th").length;
            noResultsRow = document.createElement("tr");
            noResultsRow.className = "no-results-row";
            noResultsRow.innerHTML = `
                <td colspan="${colCount}" class="text-center py-5 text-muted">
                    <i class="fa-solid fa-magnifying-glass-chart mb-3 d-block fa-2x opacity-25"></i>
                    No teams found matching "<strong>${input.value}</strong>"
                </td>
            `;
            tbody.appendChild(noResultsRow);
        }
    } else if (noResultsRow) {
        noResultsRow.remove();
    }
};

// Event listener for search input
['keyup', 'search', 'input'].forEach(evt => {
    document.addEventListener(evt, (event) => {
        if (event.target.id === 'searchInput') {
            searchTable();
        }
    });
});