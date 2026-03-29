/**
 * Search and filter a table by a search input
 */
const searchTable = () => {
    const input = document.getElementById("searchInput");
    const table = document.getElementById("tableTeams");
    if (!input || !table) return;

    const filter = input.value.toUpperCase();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(row => {
        // Skip rows that contain header cells
        if (row.querySelector("th")) return;

        const cells = Array.from(row.querySelectorAll("td"));
        const matches = cells.some(td => 
            td.textContent.toUpperCase().includes(filter)
        );

        row.style.display = matches ? "" : "none";
    });
};

// Event listener for search input
document.addEventListener('keyup', (event) => {
    if (event.target.id === 'searchInput') {
        searchTable();
    }
});