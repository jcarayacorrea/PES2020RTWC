/**
 * AJAX calls for team stage updates
 */

/**
 * Update team progress through AJAX
 * @param {string} code - Team code (nation_iso_code)
 * @param {string} stage - Stage to update to
 */
const changeTeamStage = async (code, stage) => {
    try {
        const csrftoken = getCookie('csrftoken');
        // Use a more robust way to build the URL or handle relative paths
        const url = `updateProgress/${code}/${stage}`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error(`Error updating team stage: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Network error updating team stage:', error);
    }
};

// Event delegation for team stage updates
document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action="change-team-stage"]');
    if (target) {
        const { teamCode, stage } = target.dataset;
        if (teamCode && stage) {
            changeTeamStage(teamCode, stage);
        }
    }
});



