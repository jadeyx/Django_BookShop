document.addEventListener("DOMContentLoaded", function () {
    const avatarButton = document.getElementById('avatarButton');
    const sidebar = document.getElementById('sidebar');
    const closeButton = document.getElementById('closeButton');

    avatarButton.addEventListener('click', function () {
        sidebar.style.width = '250px';
    });

    closeButton.addEventListener('click', function () {
        sidebar.style.width = '0';
    });

    window.addEventListener('click', function (event) {
        if (event.target === sidebar) {
            sidebar.style.width = '0';
        }
    });
});
