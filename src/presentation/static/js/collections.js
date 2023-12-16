function init() {
  document
    .getElementById('create-collection')
    .addEventListener('submit', function (e) {
      e.preventDefault();
      let name = document.getElementById('create-collection-name').value;

      fetch('/api/v1/collection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          window.location.href = '/collection/' + data._id;
        })
        .catch((error) => {
          console.log(error);
        });
    });
}
