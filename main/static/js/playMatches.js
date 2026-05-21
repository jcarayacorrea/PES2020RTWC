/**
 * Play a single match via AJAX
 */
const playMatch = (button) => {
    const url = button.getAttribute('data-sim-url');
    if (!url || button.disabled) return;

    const card = button.closest('.match-border');
    if (!card) return;

    button.disabled = true;
    const loadingEl = card.querySelector('.match-loading');
    const scoreEl = card.querySelector('.match-score');
    if (loadingEl) loadingEl.classList.remove('d-none');
    if (loadingEl) loadingEl.classList.add('d-flex');
    if (scoreEl) scoreEl.classList.add('d-none');

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Match simulation failed');
            return response.text();
        })
        .then(html => {
            card.innerHTML = html;
        })
        .catch(error => {
            console.error('Error playing match:', error);
            button.disabled = false;
            if (loadingEl) loadingEl.classList.add('d-none');
            if (loadingEl) loadingEl.classList.remove('d-flex');
            if (scoreEl) scoreEl.classList.remove('d-none');
        });
};

/**
 * Play all matches in the fixtures list sequentially
 */
const playMatches = () => {
    const btnExec = document.getElementById('btnExec');
    const rotateOnDiv = document.getElementById('rotateOnDiv');
    const rotateOffDiv = document.getElementById('rotateOffDiv');

    if (btnExec) btnExec.disabled = true;
    if (rotateOnDiv) rotateOnDiv.style.display = "block";
    if (rotateOffDiv) rotateOffDiv.style.display = "none";

    const buttons = document.querySelectorAll('#fixtures .match-play-btn:not([disabled])');
    let index = 0;
    const playNext = () => {
        if (index >= buttons.length) {
            if (btnExec) btnExec.disabled = false;
            if (rotateOnDiv) rotateOnDiv.style.display = "none";
            if (rotateOffDiv) rotateOffDiv.style.display = "block";
            return;
        }
        playMatch(buttons[index]);
        index++;
        setTimeout(playNext, 600);
    };
    playNext();
};

// Event delegation for individual match play buttons
document.addEventListener('click', (event) => {
    const button = event.target.closest('.match-play-btn');
    if (button) {
        playMatch(button);
    }
});

// Event listener for play all matches button
document.addEventListener('click', (event) => {
    const btn = event.target.closest('#btnExec');
    if (btn) {
        playMatches();
    }
});
