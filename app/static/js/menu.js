document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleSidebar = document.getElementById('toggleSidebar');
    const closeButton = document.getElementById('closeSidebar');

    toggleSidebar.addEventListener('click', function () {
        sidebar.classList.toggle('-translate-x-full');
    });

    closeButton.addEventListener('click', () => {
        sidebar.classList.add('-translate-x-full');  // Oculta el sidebar
    });

});
