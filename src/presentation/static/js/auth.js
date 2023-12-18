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
    url: '/auth/login?remember=' + rememberCheck,
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (data) {
      window.location.href = '/';
    },
    failure: function (errMsg) {
      alert(errMsg);
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
    url: '/auth/register?remember=' + rememberCheck,
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (data) {
      window.location.href = '/';
    },
    failure: function (errMsg) {
      alert(errMsg);
    },
  });
});
