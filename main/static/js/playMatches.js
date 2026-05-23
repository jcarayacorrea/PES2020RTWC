/**
 * Play a single match via AJAX (returns a Promise)
 */
const playMatch = (button) => {
    return new Promise((resolve) => {
        const url = button.getAttribute('data-sim-url');
        if (!url || button.disabled) {
            resolve();
            return;
        }

        const card = button.closest('.match-border');
        if (!card) {
            resolve();
            return;
        }

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
            })
            .finally(() => resolve());
    });
};

/**
 * Play all matches grouped by fixture, with 1s delay between fixtures
 */
const playMatches = async () => {
    const btnExec = document.getElementById('btnExec');
    const rotateOnDiv = document.getElementById('rotateOnDiv');
    const rotateOffDiv = document.getElementById('rotateOffDiv');

    if (btnExec) btnExec.disabled = true;
    if (rotateOnDiv) rotateOnDiv.classList.remove('d-none');
    if (rotateOffDiv) rotateOffDiv.classList.add('d-none');

    const fixtureCards = document.querySelectorAll('#fixtures .fixture-card');
    const totalFixtures = fixtureCards.length;
    let completedFixtures = 0;

    for (const fixtureCard of fixtureCards) {
        const buttons = fixtureCard.querySelectorAll('.match-play-btn:not([disabled])');
        const promises = Array.from(buttons).map(btn => playMatch(btn));
        await Promise.all(promises);
        completedFixtures++;
        if (completedFixtures < totalFixtures) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    if (btnExec) btnExec.disabled = false;
    if (rotateOnDiv) rotateOnDiv.classList.add('d-none');
    if (rotateOffDiv) rotateOffDiv.classList.remove('d-none');
};

/**
 * Play all matches within a stage card container
 */
const playStageMatches = async (button) => {
    const card = button.closest('.card.card-border');
    if (!card) return;

    const stage = button.getAttribute('data-playall-stage');
    const offEl = card.querySelector(`[data-playall-off="${stage}"]`);
    const onEl = card.querySelector(`[data-playall-on="${stage}"]`);

    button.disabled = true;
    if (onEl) onEl.classList.remove('d-none');
    if (offEl) offEl.classList.add('d-none');

    const buttons = card.querySelectorAll('.match-play-btn:not([disabled])');
    await Promise.all(Array.from(buttons).map(btn => playMatch(btn)));

    button.disabled = false;
    if (onEl) onEl.classList.add('d-none');
    if (offEl) offEl.classList.remove('d-none');
};

// Event delegation for all button clicks
document.addEventListener('click', (event) => {
    const playBtn = event.target.closest('.match-play-btn');
    if (playBtn) {
        playMatch(playBtn);
        return;
    }
    const allBtn = event.target.closest('#btnExec');
    if (allBtn) {
        playMatches();
        return;
    }
    const stageBtn = event.target.closest('[data-playall-stage]');
    if (stageBtn) {
        playStageMatches(stageBtn);
    }
});
