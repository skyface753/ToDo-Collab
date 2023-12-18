let toggleButton = document.getElementById('toggle-button');
let navbarDefault = document.getElementById('navbar-default');

toggleButton.addEventListener('click', function () {
  navbarDefault.classList.toggle('hidden');
});
