$('#login-btn').click(function (event) {
  event.preventDefault();
  const username = $('#username').val();
  const password = $('#password').val();
  const rememberCheck = $('#rememberCheck').is(':checked');
  const data = {
    name: username,
    password: password,
  };
  $.ajax({
    type: 'POST',
    url: '/api/v1/user/login?remember=' + rememberCheck,
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (data) {
      window.location.href = '/';
    },
    error: function (xhr, status, error) {
      setErrorMsg(xhr.responseText);
    },
  });
});
$('#register-btn').click(function (event) {
  event.preventDefault();
  const username = $('#username').val();
  const password = $('#password').val();
  const rememberCheck = $('#rememberCheck').is(':checked');
  // Print the values
  console.log(username);
  console.log(password);
  const data = {
    name: username,
    password: password,
  };
  $.ajax({
    type: 'POST',
    url: '/api/v1/user/register?remember=' + rememberCheck,
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (data) {
      window.location.href = '/';
    },
    error: function (xhr, status, error) {
      setErrorMsg(xhr.responseText);
    },
  });
});

// Set error message
function setErrorMsg(error) {
  console.log(error);
  try {
    error = JSON.parse(error);
    error = error.detail;
  } catch {
    error = 'Something went wrong';
  }
  $('#error-msg').text(error);
  $('#error-msg-container').addClass('flex');
  $('#error-msg-container').removeClass('hidden');
}
