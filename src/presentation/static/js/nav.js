var toggleButton = document.getElementById('toggle-button');
var navbarDefault = document.getElementById('navbar-default');

toggleButton.addEventListener('click', function () {
  navbarDefault.classList.toggle('hidden');
});
