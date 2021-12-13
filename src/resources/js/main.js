export function showLoader() {
    document.querySelector('#loader').classList.remove('d-none');
}

export function hideLoader() {
    document.querySelector('#loader').classList.add('d-none');
}

// initialize modal
document.addEventListener('DOMContentLoaded', function () {
    var modalEl = document.querySelector('#modal');
    window.modal = new bootstrap.Modal(modalEl);

    window.modal.hide();

    document.addEventListener('transportSaved', function () {
        window.modal.hide();
    });
}, { once: true });

document.addEventListener('htmx:afterRequest', function () {
    hideLoader();
});

document.addEventListener('htmx:beforeSend', function () {
    showLoader();
});

// used to inject csrf token into post requests
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
