/**
 * Play all matches in the fixtures list
 */
const playMatches = () => {
    const btnExec = document.getElementById('btnExec');
    const rotateOnDiv = document.getElementById('rotateOnDiv');
    const rotateOffDiv = document.getElementById('rotateOffDiv');

    if (btnExec) btnExec.disabled = true;
    if (rotateOnDiv) rotateOnDiv.style.display = "block";
    if (rotateOffDiv) rotateOffDiv.style.display = "none";

    // Get all fixture buttons that are not disabled and click them
    const buttons = document.querySelectorAll('#fixtures button:not([disabled])');
    buttons.forEach(button => {
        button.click();
    });
};

// Event listener for play matches button
document.addEventListener('click', (event) => {
    // Check if the click was on the button or any of its children
    const btn = event.target.closest('#btnExec');
    if (btn) {
        playMatches();
    }
});

