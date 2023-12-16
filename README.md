# PRG

Post requests always return status code 303, with the location header set to the URL of the newly created resource. This is a redirect, and the browser will make a GET request to the new URL. This is called the Post/Redirect/Get pattern.
So jinja2(html) can easy use forms to send data to server, and server can redirect to another page.

The object with also returned as a JSON object, so you can use it in your JavaScript code.
