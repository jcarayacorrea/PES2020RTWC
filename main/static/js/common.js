/**
 * Common utility functions and HTMX configuration
 */

/**
 * Get cookie value by name
 * @param {string} name - Name of the cookie
 * @returns {string|null} - Value of the cookie or null if not found
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// HTMX configuration for CSRF
document.body.addEventListener('htmx:configRequest', (event) => {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        event.detail.headers['X-CSRFToken'] = csrftoken;
    }
});
