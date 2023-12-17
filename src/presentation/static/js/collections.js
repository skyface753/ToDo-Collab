function init() {
  window.addEventListener('pageshow', function (event) {
    const historyTraversal =
      event.persisted ||
      (typeof window.performance != 'undefined' &&
        window.performance.getEntriesByType('navigation').length &&
        window.performance.getEntriesByType('navigation')[0].type ===
          'back_forward');
    if (historyTraversal) {
      // Handle page restore.
      window.location.reload();
    }
  });

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
          window.location.href = '/collection/' + data.id;
        })
        .catch((error) => {
          console.log(error);
        });
    });
}
