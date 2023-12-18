const user_name = document.getElementById('user_name');
const collection_id = document.getElementById('collection_id');
const token = document.getElementById('token');
// user_name = '{{user.name}}';
// console.log('username: ' + user_name);
var ws = new WebSocket(
  'ws://localhost:8000/api/v1/todo/ws/' +
    collection_id.value +
    '?token=' +
    token.value
);
ws.onmessage = function (event) {
  var todos = document.getElementById('todos');
  try {
    var todo = JSON.parse(event.data);
    processTodo(todo);
    console.log("Received: '" + event.data + "'");
  } catch (e) {
    console.log(event.data);
  }
};

function processTodo(todo) {
  var todos = document.getElementById('todos');
  var todoItem = document.createElement('article');
  todoItem.className = 'item';
  var todoTitle = document.createElement('h3');
  var todoDescription = document.createElement('p');
  todoTitle.textContent = todo.title;
  todoDescription.textContent = todo.description;
  todoItem.appendChild(todoTitle);
  todoItem.appendChild(todoDescription);
  todos.appendChild(todoItem);
}
function sendMessage(event) {
  var todoTitle = document.getElementById('todoTitle');
  var todoDescription = document.getElementById('todoDescription');
  // To jsson
  var todo = {
    title: todoTitle.value,
    description: todoDescription.value,
  };
  // To string
  var todoString = JSON.stringify(todo);
  ws.send(todoString);
  todoTitle.value = '';
  todoDescription.value = '';
  event.preventDefault();
}
async function addToCollection(event) {
  event.preventDefault();
  // Send to server put with fetch
  var user_name_to_add = document.getElementById('user_name_to_add');
  var user_name_to_add_value = user_name_to_add.value;
  var url = '/api/v1/member/create';
  var data = {
    user_name: user_name_to_add_value,
    collection_id: collection_id.value,
  };
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.redirected) {
        alert('User already in collection');
      } else {
        return response;
      }
    })
    .catch((error) => {
      console.log(error);
    });

  const content = await response.json();
  console.log(content);
  user_name_to_add.value = '';
}
