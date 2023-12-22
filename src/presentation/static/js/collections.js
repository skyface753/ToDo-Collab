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

  // document
  //   .getElementById('create-collection-form')
  //   .addEventListener('submit', function (e) {
  //     e.preventDefault();
  //     let name = document.getElementById('create-collection-name').value;

  //     fetch('/api/v1/collection', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({
  //         name: name,
  //       }),
  //     })
  //       .then((response) => {
  //         if (response.status === 201) {
  //           return response.json();
  //         } else {
  //           throw new Error('Something went wrong');
  //         }
  //       })
  //       .then((data) => {
  //         if (data.id) window.location.href = '/collection/' + data.id;
  //       })
  //       .catch((error) => {
  //         var errorMsgField = document.getElementById(
  //           'create-collection-error'
  //         );
  //         errorMsgField.innerText = error;
  //         console.log(error);
  //       });
  //   });
}

function showCreateCollectionOverlay() {
  document.getElementById('overlay').style.display = 'block';
}

function hideCreateCollectionOverlay() {
  document.getElementById('overlay').style.display = 'none';
}

$('#create-collection-form').submit(function (event) {
  event.preventDefault();
  const name = $('#create-collection-name').val();
  const data = {
    name: name,
  };
  $.ajax({
    type: 'POST',
    url: '/api/v1/collection',
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (data) {
      window.location.href = '/collection/' + data.id;
    },
    error: function (xhr, textStatus, error) {
      let errorMsg = 'Something went wrong';
      console.log(xhr.responseText);
      console.log(error);
      if (error === 'Unprocessable Entity') {
        errorMsg = 'Collection name must be at least 1 character long';
      } else {
        error = JSON.parse(xhr.responseText);
        if (error.detail) {
          errorMsg = error.detail;
        }
      }

      $('#create-collection-error').text(errorMsg);
    },
  });
});

$('#create-collection-cancle').click(function (event) {
  event.preventDefault();
  hideCreateCollectionOverlay();
});
